from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AlertGroupComment(StrictSchema):
    alert_group_id: str
    short_title: str
    short_conclusion: str
    facts: list[str]
    business_interpretation: str
    possible_causes: list[str]
    recommended_checks: list[str]
    event_classification: Literal[
        "expected_event",
        "expected_process_feature",
        "potential_incident",
        "needs_manual_review",
    ]
    risk_level: Literal["low", "medium", "high"]
    confidence: Literal["low", "medium", "high"]


class InvestigationToolCall(StrictSchema):
    tool_name: str
    reason: str
    expected_evidence: str


class InvestigationToolPlan(StrictSchema):
    alert_group_id: str
    selected_tools: list[InvestigationToolCall] = Field(max_length=5)
    stop_reason: str


class ToolResult(StrictSchema):
    tool_name: str
    status: Literal["ok", "warning", "critical"]
    finding: str
    evidence: dict[str, Any]
    supports_hypothesis: bool


class InvestigationReport(StrictSchema):
    alert_group_id: str
    evidence_summary: list[str]
    root_cause_hypothesis: str
    confidence: Literal["low", "medium", "high"]
    recommended_actions: list[str]
    needs_manual_review: bool


class FinalSummary(StrictSchema):
    overall_status: Literal["ok", "warning", "critical"]
    executive_summary: str
    expected_events: list[str]
    potential_incidents: list[str]
    root_cause_hypotheses: list[str]
    priority_checks: list[str]
    manager_summary: str


# Backward-compatible names used by the first prompt architecture prototype.
SelectedTool = InvestigationToolCall
InvestigationPlan = InvestigationToolPlan
