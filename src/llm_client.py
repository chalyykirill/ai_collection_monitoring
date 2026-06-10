from __future__ import annotations

import json
import os
import re
from typing import Any, TypeVar

from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from pydantic import BaseModel, ValidationError

from src.prompts import (
    build_alert_commentator_prompt,
    build_final_summarizer_prompt,
    build_investigation_planner_prompt,
    build_investigation_summary_prompt,
    build_repair_json_prompt,
)
from src.schemas import (
    AlertGroupComment,
    FinalSummary,
    InvestigationPlan,
    InvestigationReport,
)


SchemaT = TypeVar("SchemaT", bound=BaseModel)

SYSTEM_PROMPT = """
Ты работаешь в системе мониторинга Collection.
Следуй ролевым инструкциям пользовательского промпта.
Используй только переданные данные, отделяй факты от гипотез и не показывай
внутренний ход рассуждений. Всегда возвращай только JSON по заданной схеме.
""".strip()


def _extract_json(raw_response: str) -> dict[str, Any]:
    text = raw_response.strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
        if match is None:
            raise
        value = json.loads(match.group(1))

    if not isinstance(value, dict):
        raise ValueError("GigaChat response must be a JSON object.")
    return value


class GigaChatClient:
    def __init__(
        self,
        credentials: str | None = None,
        scope: str | None = None,
        verify_ssl_certs: bool = False,
        model: str | None = None,
    ) -> None:
        load_dotenv()
        self.credentials = credentials or os.getenv("GIGACHAT_CREDENTIALS")
        if not self.credentials:
            raise ValueError("GIGACHAT_CREDENTIALS is not configured.")

        self.scope = scope or os.getenv(
            "GIGACHAT_SCOPE",
            "GIGACHAT_API_PERS",
        )
        self.verify_ssl_certs = verify_ssl_certs
        self.model = model or os.getenv("GIGACHAT_MODEL")

    def generate_json(
        self,
        prompt: str,
        target_model: type[SchemaT],
    ) -> SchemaT:
        raw_response = self._chat(
            prompt=prompt,
            target_schema=target_model.model_json_schema(),
        )
        try:
            return target_model.model_validate(_extract_json(raw_response))
        except (json.JSONDecodeError, ValueError, ValidationError) as error:
            repair_prompt = build_repair_json_prompt(
                raw_response=raw_response,
                validation_error=str(error),
                target_schema=target_model.model_json_schema(),
            )
            repaired_response = self._chat(
                prompt=repair_prompt,
                target_schema=target_model.model_json_schema(),
            )
            return target_model.model_validate(_extract_json(repaired_response))

    def comment_alert_group(
        self,
        alert_group: dict[str, Any],
        doc_context: str = "",
        examples: list[dict] | None = None,
    ) -> AlertGroupComment:
        prompt = build_alert_commentator_prompt(
            alert_group=alert_group,
            doc_context=doc_context,
            examples=examples,
        )
        comment = self.generate_json(prompt, AlertGroupComment)
        if comment.alert_group_id != alert_group["alert_group_id"]:
            raise ValueError(
                "GigaChat returned a comment for another alert group."
            )
        return comment

    def plan_investigation(
        self,
        alert_group: dict[str, Any],
        alert_comment: dict[str, Any],
        doc_context: str,
        available_tools: list[dict],
        examples: list[dict] | None = None,
    ) -> InvestigationPlan:
        prompt = build_investigation_planner_prompt(
            alert_group=alert_group,
            alert_comment=alert_comment,
            doc_context=doc_context,
            available_tools=available_tools,
            examples=examples,
        )
        return self.generate_json(prompt, InvestigationPlan)

    def summarize_investigation(
        self,
        alert_group: dict[str, Any],
        alert_comment: dict[str, Any],
        tool_results: list[dict],
        doc_context: str,
        examples: list[dict] | None = None,
    ) -> InvestigationReport:
        prompt = build_investigation_summary_prompt(
            alert_group=alert_group,
            alert_comment=alert_comment,
            tool_results=tool_results,
            doc_context=doc_context,
            examples=examples,
        )
        return self.generate_json(prompt, InvestigationReport)

    def summarize_monitoring(
        self,
        monitoring_stats: dict[str, Any],
        alert_group_comments: list[dict],
        investigation_reports: list[dict],
        doc_context: str,
        examples: list[dict] | None = None,
    ) -> FinalSummary:
        prompt = build_final_summarizer_prompt(
            monitoring_stats=monitoring_stats,
            alert_group_comments=alert_group_comments,
            investigation_reports=investigation_reports,
            doc_context=doc_context,
            examples=examples,
        )
        return self.generate_json(prompt, FinalSummary)

    def _chat(self, prompt: str, target_schema: dict[str, Any]) -> str:
        payload = Chat(
            model=self.model,
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT),
                Messages(role=MessagesRole.USER, content=prompt),
            ],
            temperature=0.1,
            max_tokens=1600,
            response_format={
                "type": "json_schema",
                "schema": target_schema,
                "strict": True,
            },
        )
        with GigaChat(
            credentials=self.credentials,
            scope=self.scope,
            verify_ssl_certs=self.verify_ssl_certs,
            model=self.model,
        ) as client:
            response = client.chat(payload)

        content = response.choices[0].message.content
        if not content:
            raise ValueError("GigaChat returned an empty response.")
        return content
