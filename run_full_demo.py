import html
import json
import re
import subprocess
import sys
from pathlib import Path

from src.llm_client import _contains_english_sentence


RUN_DIR = Path("outputs/runs/demo_run")
REPORT_PATH = RUN_DIR / "human_report.html"
FINAL_SUMMARY_PATH = RUN_DIR / "final_summary.json"
INVESTIGATIONS_PATH = RUN_DIR / "investigation_reports.json"
STEPS = [
    "run_pipeline.py",
    "run_gigachat_comments.py",
    "run_investigations.py",
    "run_final_summary.py",
    "run_build_report.py",
]


def _load_json(path: Path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"Final demo audit failed: {message}")


def _visible_html_text(document: str) -> list[str]:
    without_code = re.sub(
        r"<(style|script).*?</\1>",
        "",
        document,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return [
        html.unescape(text).strip()
        for text in re.findall(r">([^<>]+)<", without_code)
        if html.unescape(text).strip()
    ]


def run_final_audit() -> None:
    required_paths = [
        REPORT_PATH,
        FINAL_SUMMARY_PATH,
        INVESTIGATIONS_PATH,
    ]
    for path in required_paths:
        _require(path.exists(), f"missing artifact {path.as_posix()}")

    alert_groups = _load_json(RUN_DIR / "alert_groups.json")
    comments = _load_json(RUN_DIR / "alert_group_comments.json")
    investigations = _load_json(INVESTIGATIONS_PATH)
    final_summary = _load_json(FINAL_SUMMARY_PATH)

    _require(len(alert_groups) == 6, "expected 6 alert groups")
    _require(len(comments) == 6, "expected 6 alert group comments")
    _require(
        len(investigations) == 6,
        "expected 6 investigation reports",
    )
    chart_count = len(list((RUN_DIR / "charts").glob("*.png")))
    _require(chart_count >= 10, "expected at least 10 PNG charts")

    expected_classifications = {
        "expected_event",
        "expected_process_feature",
    }
    incident_classifications = {
        "potential_incident",
        "needs_manual_review",
    }
    expected_ids = [
        comment["alert_group_id"]
        for comment in comments
        if comment.get("event_classification")
        in expected_classifications
    ]
    incident_ids = [
        comment["alert_group_id"]
        for comment in comments
        if comment.get("event_classification")
        in incident_classifications
    ]
    _require(len(expected_ids) == 2, "expected events count must be 2")
    _require(
        len(incident_ids) == 4,
        "potential incidents count must be 4",
    )
    _require(
        final_summary.get("expected_events") == expected_ids,
        "final_summary.expected_events is inconsistent with comments",
    )
    _require(
        final_summary.get("potential_incidents") == incident_ids,
        "final_summary.potential_incidents is inconsistent with comments",
    )

    document = REPORT_PATH.read_text(encoding="utf-8")
    _require(
        "placeholder" not in document.lower(),
        "HTML contains placeholder text",
    )
    _require(
        "ожидаемый инцидент" not in document.lower(),
        "expected event is described as an incident",
    )
    english_text = [
        text
        for text in _visible_html_text(document)
        if _contains_english_sentence(text)
    ]
    _require(
        not english_text,
        f"HTML contains English prose: {english_text[:3]}",
    )

    summary_start = document.find("<h2>Итоговое резюме</h2>")
    summary_end = document.find("<h2>Статистика мониторинга</h2>")
    _require(
        summary_start >= 0 and summary_end > summary_start,
        "executive summary section was not found",
    )
    executive_section = document[summary_start:summary_end]
    group_by_id = {
        group["alert_group_id"]: group
        for group in alert_groups
    }
    expected_event_types = {
        group_by_id[group_id]["event_type"]
        for group_id in expected_ids
    }
    required_event_types = {
        "bank_unavailable_day",
        "credit_card_batch_inflow",
    }
    _require(
        required_event_types <= expected_event_types,
        "expected demo events are not classified as expected",
    )
    for event_type in required_event_types:
        _require(
            event_type in executive_section,
            f"{event_type} is missing from executive summary",
        )

    print(
        "Final audit passed: "
        f"groups={len(alert_groups)}, comments={len(comments)}, "
        f"investigations={len(investigations)}, charts={chart_count}, "
        f"expected={len(expected_ids)}, incidents={len(incident_ids)}."
    )


def main() -> None:
    for step in STEPS:
        print(f"\n=== Running {step} ===", flush=True)
        subprocess.run([sys.executable, step], check=True)

    print("\n=== Running final audit ===", flush=True)
    run_final_audit()

    print("\nDemo completed.")
    print(f"Report: {REPORT_PATH.as_posix()}")


if __name__ == "__main__":
    main()
