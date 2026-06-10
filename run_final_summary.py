import json
from pathlib import Path

from src.llm_client import GigaChatClient
from src.schemas import FinalSummary


RUN_DIR = Path("outputs/runs/demo_run")
OUTPUT_PATH = RUN_DIR / "final_summary.json"


def _load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise ValueError(f"Expected a JSON list in {path}.")
    return value


def _monitoring_stats(
    alert_groups: list[dict],
    comments: list[dict],
) -> dict:
    classifications = [
        comment.get("event_classification")
        for comment in comments
    ]
    return {
        "alert_groups": len(alert_groups),
        "critical_groups": sum(
            group.get("critical_count", 0) > 0
            for group in alert_groups
        ),
        "warning_groups": sum(
            group.get("critical_count", 0) == 0
            and group.get("warning_count", 0) > 0
            for group in alert_groups
        ),
        "expected_events": sum(
            classification
            in {"expected_event", "expected_process_feature"}
            for classification in classifications
        ),
        "potential_incidents": sum(
            classification
            in {"potential_incident", "needs_manual_review"}
            for classification in classifications
        ),
        "needs_manual_review": classifications.count(
            "needs_manual_review"
        ),
    }


def _short_doc_context(retrieved_contexts: list[dict]) -> str:
    lines: list[str] = []
    seen_sources: set[str] = set()
    for context in retrieved_contexts:
        for chunk in context.get("chunks", []):
            source = str(chunk.get("source", "unknown"))
            if source in seen_sources:
                continue
            seen_sources.add(source)
            preview = str(chunk.get("text_preview", "")).strip()
            lines.append(f"[{source}] {preview[:350]}")
    return "\n\n".join(lines[:10])


def _compact_investigations(
    investigations: list[dict],
) -> list[dict]:
    compact: list[dict] = []
    for investigation in investigations:
        compact.append(
            {
                "alert_group_id": investigation["alert_group_id"],
                "tool_findings": [
                    {
                        "tool_name": result.get("tool_name"),
                        "status": result.get("status"),
                        "finding": result.get("finding"),
                        "supports_hypothesis": result.get(
                            "supports_hypothesis"
                        ),
                    }
                    for result in investigation.get("tool_results", [])
                ],
                "investigation_report": investigation.get(
                    "investigation_report",
                    {},
                ),
            }
        )
    return compact


def main() -> None:
    comments = _load_json(RUN_DIR / "alert_group_comments.json")
    investigations = _load_json(RUN_DIR / "investigation_reports.json")
    retrieved_contexts = _load_json(
        RUN_DIR / "retrieved_contexts.json"
    )
    alert_groups = _load_json(RUN_DIR / "alert_groups.json")

    summary = GigaChatClient().summarize_monitoring(
        monitoring_stats=_monitoring_stats(alert_groups, comments),
        alert_group_comments=comments,
        investigation_reports=_compact_investigations(investigations),
        doc_context=_short_doc_context(retrieved_contexts),
    )
    FinalSummary.model_validate(summary.model_dump())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            summary.model_dump(),
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Final summary saved: {OUTPUT_PATH.as_posix()}")


if __name__ == "__main__":
    main()

