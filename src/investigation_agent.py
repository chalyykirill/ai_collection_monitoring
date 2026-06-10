from __future__ import annotations

from typing import Any

import pandas as pd

from src.diagnostic_tools import TOOL_REGISTRY, get_available_tools
from src.schemas import (
    InvestigationToolCall,
    InvestigationToolPlan,
    ToolResult,
)


def _filter_tool_plan(
    tool_plan: InvestigationToolPlan,
) -> InvestigationToolPlan:
    selected_tools: list[InvestigationToolCall] = []
    seen: set[str] = set()

    for tool_call in tool_plan.selected_tools:
        if tool_call.tool_name not in TOOL_REGISTRY:
            continue
        if tool_call.tool_name in seen:
            continue
        selected_tools.append(tool_call)
        seen.add(tool_call.tool_name)
        if len(selected_tools) == 5:
            break

    return InvestigationToolPlan(
        alert_group_id=tool_plan.alert_group_id,
        selected_tools=selected_tools,
        stop_reason=tool_plan.stop_reason,
    )


def _execute_tool(
    tool_name: str,
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> ToolResult:
    try:
        raw_result = TOOL_REGISTRY[tool_name](monitoring_df, alert_group)
    except Exception as error:
        raw_result = {
            "tool_name": tool_name,
            "status": "warning",
            "finding": f"Выполнение инструмента завершилось ошибкой: {error}",
            "evidence": {},
            "supports_hypothesis": False,
        }
    return ToolResult.model_validate(raw_result)


def run_investigation_for_group(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
    alert_comment: dict,
    rag_context: str,
    llm_client: Any,
) -> dict:
    tool_plan = llm_client.plan_investigation(
        alert_group=alert_group,
        alert_comment=alert_comment,
        doc_context=rag_context,
        available_tools=get_available_tools(),
    )
    filtered_plan = _filter_tool_plan(tool_plan)

    tool_results = [
        _execute_tool(
            tool_call.tool_name,
            monitoring_df,
            alert_group,
        )
        for tool_call in filtered_plan.selected_tools
    ]
    investigation_report = llm_client.summarize_investigation(
        alert_group=alert_group,
        alert_comment=alert_comment,
        tool_results=[result.model_dump() for result in tool_results],
        doc_context=rag_context,
    )

    return {
        "alert_group_id": alert_group["alert_group_id"],
        "tool_plan": filtered_plan.model_dump(),
        "tool_results": [result.model_dump() for result in tool_results],
        "investigation_report": investigation_report.model_dump(),
    }
