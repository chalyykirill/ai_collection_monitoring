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
    build_final_summary_consistency_repair_prompt,
    build_final_summarizer_prompt,
    build_investigation_planner_prompt,
    build_investigation_summary_prompt,
    build_repair_json_prompt,
    build_translate_json_to_russian_prompt,
)
from src.schemas import (
    AlertGroupComment,
    FinalSummary,
    InvestigationToolPlan,
    InvestigationReport,
)


SchemaT = TypeVar("SchemaT", bound=BaseModel)

TECHNICAL_LATIN_WORDS = {
    "alert",
    "api",
    "collection",
    "critical",
    "data",
    "dpd",
    "event",
    "feature",
    "gini",
    "high",
    "info",
    "json",
    "llm",
    "low",
    "medium",
    "model",
    "null",
    "ok",
    "pp",
    "psi",
    "python",
    "rate",
    "reject",
    "risk",
    "score",
    "share",
    "target",
    "tool",
    "vector",
    "warning",
}

TECHNICAL_VALUES = {
    "expected_event",
    "expected_process_feature",
    "potential_incident",
    "needs_manual_review",
    "low",
    "medium",
    "high",
    "ok",
    "warning",
    "critical",
}

EXPECTED_CLASSIFICATIONS = {
    "expected_event",
    "expected_process_feature",
}
INCIDENT_CLASSIFICATIONS = {
    "potential_incident",
    "needs_manual_review",
}

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


def _is_technical_value(value: str) -> bool:
    stripped = value.strip()
    if stripped in TECHNICAL_VALUES:
        return True
    if re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)+", stripped):
        return True
    if stripped.startswith("alert_group_"):
        return True
    return False


def _contains_english_sentence(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_english_sentence(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_english_sentence(item) for item in value)
    if not isinstance(value, str) or _is_technical_value(value):
        return False

    latin_words = re.findall(r"\b[A-Za-z]{2,}\b", value)
    nontechnical_words = [
        word
        for word in latin_words
        if word.lower() not in TECHNICAL_LATIN_WORDS
    ]
    cyrillic_letters = len(re.findall(r"[А-Яа-яЁё]", value))
    if cyrillic_letters == 0:
        return len(latin_words) >= 3 and len(nontechnical_words) >= 2
    return len(nontechnical_words) >= 5


def _classified_group_ids(
    alert_group_comments: list[dict],
) -> tuple[list[str], list[str]]:
    expected_ids: list[str] = []
    incident_ids: list[str] = []
    for comment in alert_group_comments:
        group_id = str(comment["alert_group_id"])
        classification = comment.get("event_classification")
        if classification in EXPECTED_CLASSIFICATIONS:
            expected_ids.append(group_id)
        elif classification in INCIDENT_CLASSIFICATIONS:
            incident_ids.append(group_id)
    return expected_ids, incident_ids


def _final_summary_consistency_errors(
    summary: FinalSummary,
    expected_ids: list[str],
    incident_ids: list[str],
) -> list[str]:
    errors: list[str] = []
    if summary.expected_events != expected_ids:
        errors.append(
            "expected_events должен точно совпадать со списком "
            f"{expected_ids}, получен {summary.expected_events}."
        )
    if summary.potential_incidents != incident_ids:
        errors.append(
            "potential_incidents должен точно совпадать со списком "
            f"{incident_ids}, получен {summary.potential_incidents}."
        )
    return errors


def _gini_drop_statement(alert_group: dict[str, Any]) -> str | None:
    alerts = [
        alert_group.get("main_alert", {}),
        *alert_group.get("related_alerts", []),
    ]
    gini_alert = next(
        (alert for alert in alerts if alert.get("metric") == "gini"),
        None,
    )
    if not gini_alert:
        return None

    delta_abs = gini_alert.get("delta_abs")
    threshold_abs = gini_alert.get("threshold_abs")
    if delta_abs is None or threshold_abs is None:
        return None
    return (
        f"Снижение Gini составило {abs(float(delta_abs)):.4f} и превысило "
        f"порог значимого падения {float(threshold_abs):.2f}."
    )


def _has_gini_threshold_misstatement(text: str) -> bool:
    normalized = text.lower()
    return (
        "gini" in normalized
        and "порог" in normalized
        and ("ниже" in normalized or "меньше" in normalized)
    )


def _ensure_gini_drop_statement(
    items: list[str],
    statement: str,
) -> list[str]:
    polished: list[str] = []
    statement_added = False
    for item in items:
        normalized = item.lower()
        is_threshold_statement = (
            "порог" in normalized
            and ("gini" in normalized or "delta_abs" in normalized)
        )
        if _has_gini_threshold_misstatement(item) or is_threshold_statement:
            if not statement_added:
                polished.append(statement)
                statement_added = True
            continue
        polished.append(_clean_sentence(item))
    if not statement_added:
        polished.append(statement)
    return polished


def _clean_sentence(text: str) -> str:
    return text.replace("п.п..", "п.п.")


def _polish_alert_comment_semantics(
    comment: AlertGroupComment,
    alert_group: dict[str, Any],
) -> AlertGroupComment:
    if alert_group.get("event_type") != "model_gini_drop":
        return comment

    statement = _gini_drop_statement(alert_group)
    if statement is None:
        return comment
    facts = _ensure_gini_drop_statement(comment.facts, statement)
    return comment.model_copy(update={"facts": facts})


def _polish_investigation_semantics(
    report: InvestigationReport,
    alert_group: dict[str, Any],
    alert_comment: dict[str, Any],
) -> InvestigationReport:
    event_type = alert_group.get("event_type")
    classification = alert_comment.get("event_classification")
    update: dict[str, Any] = {
        "evidence_summary": [
            _clean_sentence(item)
            for item in report.evidence_summary
        ],
        "root_cause_hypothesis": _clean_sentence(
            report.root_cause_hypothesis
        ),
        "recommended_actions": [
            _clean_sentence(item)
            for item in report.recommended_actions
        ],
    }

    if event_type == "model_gini_drop":
        statement = _gini_drop_statement(alert_group)
        if statement is not None:
            update["evidence_summary"] = _ensure_gini_drop_statement(
                report.evidence_summary,
                statement,
            )

    if classification in EXPECTED_CLASSIFICATIONS:
        if event_type == "credit_card_batch_inflow":
            update.update(
                {
                    "root_cause_hypothesis": (
                        "Скачок объема и доли credit_card объясняется "
                        "ожидаемым пакетным поступлением портфеля."
                    ),
                    "recommended_actions": [
                        "Контролировать завершение пакетной загрузки.",
                        (
                            "Анализировать метрики с учетом продуктового "
                            "микса."
                        ),
                    ],
                    "needs_manual_review": False,
                }
            )
        elif event_type == "bank_unavailable_day":
            update.update(
                {
                    "root_cause_hypothesis": (
                        "Критичное отклонение объема объяснено "
                        "подтвержденным ЕДН и не является инцидентом."
                    ),
                    "recommended_actions": [
                        (
                            "Контролировать восстановление потока после "
                            "завершения ЕДН."
                        )
                    ],
                    "needs_manual_review": False,
                }
            )
        else:
            update.update(
                {
                    "root_cause_hypothesis": str(
                        alert_comment.get(
                            "business_interpretation",
                            report.root_cause_hypothesis,
                        )
                    ),
                    "recommended_actions": list(
                        alert_comment.get(
                            "recommended_checks",
                            report.recommended_actions,
                        )
                    ),
                    "needs_manual_review": False,
                }
            )

    return report.model_copy(update=update)


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
        repair_on_error: bool = True,
    ) -> SchemaT:
        raw_response = self._chat(
            prompt=prompt,
            target_schema=target_model.model_json_schema(),
        )
        try:
            validated = target_model.model_validate(
                _extract_json(raw_response)
            )
        except (json.JSONDecodeError, ValueError, ValidationError) as error:
            if not repair_on_error:
                raise
            repair_prompt = build_repair_json_prompt(
                raw_response=raw_response,
                validation_error=str(error),
                target_schema=target_model.model_json_schema(),
            )
            repaired_response = self._chat(
                prompt=repair_prompt,
                target_schema=target_model.model_json_schema(),
            )
            validated = target_model.model_validate(
                _extract_json(repaired_response)
            )

        if _contains_english_sentence(validated.model_dump()):
            language_prompt = build_translate_json_to_russian_prompt(
                validated_json=validated.model_dump(),
                target_schema=target_model.model_json_schema(),
            )
            translated_response = self._chat(
                prompt=language_prompt,
                target_schema=target_model.model_json_schema(),
            )
            validated = target_model.model_validate(
                _extract_json(translated_response)
            )
        return validated

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
        return _polish_alert_comment_semantics(comment, alert_group)

    def plan_investigation(
        self,
        alert_group: dict[str, Any],
        alert_comment: dict[str, Any],
        doc_context: str,
        available_tools: list[dict],
        examples: list[dict] | None = None,
    ) -> InvestigationToolPlan:
        prompt = build_investigation_planner_prompt(
            alert_group=alert_group,
            alert_comment=alert_comment,
            doc_context=doc_context,
            available_tools=available_tools,
            examples=examples,
        )
        plan = self.generate_json(
            prompt,
            InvestigationToolPlan,
            repair_on_error=False,
        )
        if plan.alert_group_id != alert_group["alert_group_id"]:
            raise ValueError(
                "GigaChat returned an investigation plan for another group."
            )
        return plan

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
        report = self.generate_json(
            prompt,
            InvestigationReport,
            repair_on_error=False,
        )
        if report.alert_group_id != alert_group["alert_group_id"]:
            raise ValueError(
                "GigaChat returned an investigation report for another group."
            )
        return _polish_investigation_semantics(
            report,
            alert_group,
            alert_comment,
        )

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
        summary = self.generate_json(prompt, FinalSummary)
        expected_ids, incident_ids = _classified_group_ids(
            alert_group_comments
        )
        consistency_errors = _final_summary_consistency_errors(
            summary,
            expected_ids,
            incident_ids,
        )
        if consistency_errors:
            repair_prompt = build_final_summary_consistency_repair_prompt(
                final_summary=summary.model_dump(),
                alert_group_comments=alert_group_comments,
                consistency_errors=consistency_errors,
                target_schema=FinalSummary.model_json_schema(),
            )
            try:
                repaired_summary = self.generate_json(
                    repair_prompt,
                    FinalSummary,
                )
            except Exception:
                repaired_summary = None
            if repaired_summary is not None:
                if not _final_summary_consistency_errors(
                    repaired_summary,
                    expected_ids,
                    incident_ids,
                ):
                    return repaired_summary

        if consistency_errors:
            summary = summary.model_copy(
                update={
                    "expected_events": expected_ids,
                    "potential_incidents": incident_ids,
                }
            )
        return summary

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
