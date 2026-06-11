from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from src.diagnostic_tools import get_available_tools
from src.doc_context import get_event_doc_context
from src.prompts import (
    ALERT_COMMENTATOR_EXAMPLES,
    build_alert_commentator_prompt,
    build_final_summarizer_prompt,
    build_investigation_planner_prompt,
    build_investigation_summary_prompt,
)
from src.rag import retrieve_context


RUN_DIR = Path("outputs/runs/demo_run")
DOCS_DIR = Path("docs")
TRACE_DIR = RUN_DIR / "llm_io_trace"

REQUIRED_ARTIFACTS = {
    "alert_groups": RUN_DIR / "alert_groups.json",
    "comments": RUN_DIR / "alert_group_comments.json",
    "contexts": RUN_DIR / "retrieved_contexts.json",
    "investigations": RUN_DIR / "investigation_reports.json",
    "final_summary": RUN_DIR / "final_summary.json",
    "monitoring_data": RUN_DIR / "monitoring_data.csv",
}


def _load_json(path: Path, expected_type: type) -> Any:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, expected_type):
        raise ValueError(
            f"Expected {expected_type.__name__} in {path.as_posix()}."
        )
    return value


def _read_monitoring_data(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError(f"CSV header is missing in {path.as_posix()}.")
        return sum(1 for _ in reader)


def _by_group_id(items: list[dict], artifact_name: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in items:
        group_id = item.get("alert_group_id")
        if not group_id:
            raise ValueError(
                f"alert_group_id is missing in {artifact_name}."
            )
        if group_id in result:
            raise ValueError(
                f"Duplicate alert_group_id {group_id} in {artifact_name}."
            )
        result[str(group_id)] = item
    return result


def _safe_directory_name(event_type: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", event_type).strip("_")
    return value or "unknown_event"


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _markdown_trace(
    *,
    title: str,
    stage_description: str,
    prompt: str,
    output: dict,
    alert_group: dict | None = None,
    reconstruction_note: str | None = None,
) -> str:
    sections = [f"# {title}"]
    if alert_group is not None:
        sections.extend(
            [
                "## Alert group",
                (
                    f"`{alert_group.get('event_type')}` / "
                    f"`{alert_group.get('alert_group_id')}`"
                ),
            ]
        )
    sections.extend(
        [
            "## What this stage does",
            stage_description,
        ]
    )
    if reconstruction_note:
        sections.extend(
            [
                "## Reconstruction note",
                reconstruction_note,
            ]
        )
    sections.extend(
        [
            "## Model input: rendered prompt",
            f"```text\n{prompt}\n```",
            "## Model output: saved JSON",
            f"```json\n{_json_text(output)}\n```",
        ]
    )
    return "\n\n".join(sections) + "\n"


def _saved_rag_context(context: dict) -> str:
    chunks = context.get("chunks", [])
    if not chunks:
        return "Документационный контекст не найден."
    return "\n\n".join(
        (
            f"[Источник: {chunk.get('source')}; "
            f"relevance={chunk.get('score')}]\n"
            f"{chunk.get('text_preview', '')}"
        )
        for chunk in chunks
    )


def _reconstruct_commentator_context(
    alert_group: dict,
    saved_context: dict,
) -> tuple[str, str]:
    rag_result = retrieve_context(
        alert_group=alert_group,
        docs_dir=DOCS_DIR,
    )
    saved_chunks = saved_context.get("chunks", [])
    current_chunks = rag_result.get("chunks", [])
    mismatches: list[str] = []

    if saved_context.get("query") != rag_result.get("query"):
        mismatches.append("RAG query differs from the saved query")
    if len(saved_chunks) != len(current_chunks):
        mismatches.append("retrieved chunk count differs")

    for index, (saved, current) in enumerate(
        zip(saved_chunks, current_chunks),
        start=1,
    ):
        if saved.get("source") != current.get("source"):
            mismatches.append(f"chunk {index} source differs")
        if saved.get("score") != current.get("score"):
            mismatches.append(f"chunk {index} score differs")
        if saved.get("text_preview", "") != current.get("text", "")[:300]:
            mismatches.append(f"chunk {index} preview differs")

    if mismatches:
        details = "; ".join(mismatches)
        raise ValueError(
            "Exact Alert Commentator prompt cannot be reconstructed for "
            f"{alert_group['alert_group_id']}: {details}. The saved artifact "
            "contains only 300-character text previews. To guarantee future "
            "tracing, save rag_result['context_text'] with every LLM request."
        )

    context_text = (
        rag_result.get("context_text")
        or get_event_doc_context(str(alert_group.get("event_type", "normal")))
    )
    note = (
        "Полный RAG-контекст восстановлен повторным offline retrieval через "
        "`src.rag.retrieve_context`. Query, source, score и первые 300 "
        "символов каждого chunk совпали с `retrieved_contexts.json`. "
        "Исходный полный context_text отдельно в demo artifacts не "
        "сохранялся."
    )
    return context_text, note


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


def _write(path: Path, content: str, created_files: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created_files.append(path)


def _write_group_traces(
    alert_groups: list[dict],
    comments_by_id: dict[str, dict],
    contexts_by_id: dict[str, dict],
    investigations_by_id: dict[str, dict],
    created_files: list[Path],
) -> None:
    available_tools = get_available_tools()
    for alert_group in alert_groups:
        group_id = str(alert_group["alert_group_id"])
        event_type = str(alert_group.get("event_type", "unknown_event"))
        if group_id not in comments_by_id:
            raise ValueError(f"Saved comment is missing for {group_id}.")
        if group_id not in contexts_by_id:
            raise ValueError(f"Saved RAG context is missing for {group_id}.")
        if group_id not in investigations_by_id:
            raise ValueError(
                f"Saved investigation is missing for {group_id}."
            )

        comment = comments_by_id[group_id]
        saved_context = contexts_by_id[group_id]
        investigation = investigations_by_id[group_id]
        group_dir = TRACE_DIR / _safe_directory_name(event_type)

        commentator_context, reconstruction_note = (
            _reconstruct_commentator_context(alert_group, saved_context)
        )
        commentator_prompt = build_alert_commentator_prompt(
            alert_group=alert_group,
            doc_context=commentator_context,
            examples=ALERT_COMMENTATOR_EXAMPLES,
        )
        _write(
            group_dir / "01_alert_commentator.md",
            _markdown_trace(
                title="Alert Commentator",
                alert_group=alert_group,
                stage_description=(
                    "Первичная интерпретация alert group с учетом "
                    "RAG-контекста."
                ),
                reconstruction_note=reconstruction_note,
                prompt=commentator_prompt,
                output=comment,
            ),
            created_files,
        )

        investigation_context = _saved_rag_context(saved_context)
        planner_prompt = build_investigation_planner_prompt(
            alert_group=alert_group,
            alert_comment=comment,
            doc_context=investigation_context,
            available_tools=available_tools,
        )
        _write(
            group_dir / "02_investigation_planner.md",
            _markdown_trace(
                title="Investigation Planner",
                alert_group=alert_group,
                stage_description=(
                    "Выбор diagnostic tools из whitelist для расследования "
                    "alert group."
                ),
                prompt=planner_prompt,
                output=investigation.get("tool_plan", {}),
            ),
            created_files,
        )

        summarizer_prompt = build_investigation_summary_prompt(
            alert_group=alert_group,
            alert_comment=comment,
            tool_results=investigation.get("tool_results", []),
            doc_context=investigation_context,
        )
        _write(
            group_dir / "03_investigation_summarizer.md",
            _markdown_trace(
                title="Investigation Summarizer",
                alert_group=alert_group,
                stage_description=(
                    "Интерпретация результатов diagnostic tools и "
                    "формирование root cause hypothesis."
                ),
                reconstruction_note=(
                    "Текущий builder получает `tool_results`; отдельный "
                    "`tool_plan` не входит в его сигнатуру. Названия "
                    "фактически выполненных tools присутствуют внутри "
                    "каждого tool result."
                ),
                prompt=summarizer_prompt,
                output=investigation.get("investigation_report", {}),
            ),
            created_files,
        )


def _write_common_traces(
    *,
    alert_groups: list[dict],
    comments: list[dict],
    contexts: list[dict],
    investigations: list[dict],
    final_summary: dict,
    monitoring_rows: int,
    created_files: list[Path],
) -> None:
    common_dir = TRACE_DIR / "_common_llm_requests"
    final_prompt = build_final_summarizer_prompt(
        monitoring_stats=_monitoring_stats(alert_groups, comments),
        alert_group_comments=comments,
        investigation_reports=_compact_investigations(investigations),
        doc_context=_short_doc_context(contexts),
    )
    _write(
        common_dir / "01_final_summarizer.md",
        _markdown_trace(
            title="Final Summarizer",
            stage_description=(
                "Формирует executive summary по всем alert groups, comments "
                "и investigation reports."
            ),
            reconstruction_note=(
                f"`monitoring_data.csv` прочитан и содержит "
                f"{monitoring_rows} строк. Текущий Final Summarizer builder "
                "не получает строки мониторинга напрямую; monitoring_stats "
                "восстановлен по той же логике, что и "
                "`run_final_summary.py`."
            ),
            prompt=final_prompt,
            output=final_summary,
        ),
        created_files,
    )
    _write(
        common_dir / "02_json_repair.md",
        "# JSON Repair\n\n"
        "JSON repair did not run in saved demo artifacts.\n",
        created_files,
    )
    _write(
        common_dir / "03_language_repair.md",
        "# Language Repair\n\n"
        "Language repair did not run in saved demo artifacts.\n",
        created_files,
    )


def main() -> None:
    for path in REQUIRED_ARTIFACTS.values():
        if not path.exists():
            raise FileNotFoundError(
                f"Required demo artifact is missing: {path.as_posix()}"
            )

    alert_groups = _load_json(
        REQUIRED_ARTIFACTS["alert_groups"],
        list,
    )
    comments = _load_json(REQUIRED_ARTIFACTS["comments"], list)
    contexts = _load_json(REQUIRED_ARTIFACTS["contexts"], list)
    investigations = _load_json(
        REQUIRED_ARTIFACTS["investigations"],
        list,
    )
    final_summary = _load_json(
        REQUIRED_ARTIFACTS["final_summary"],
        dict,
    )
    monitoring_rows = _read_monitoring_data(
        REQUIRED_ARTIFACTS["monitoring_data"]
    )

    comments_by_id = _by_group_id(comments, "alert_group_comments.json")
    contexts_by_id = _by_group_id(contexts, "retrieved_contexts.json")
    investigations_by_id = _by_group_id(
        investigations,
        "investigation_reports.json",
    )

    created_files: list[Path] = []
    _write_group_traces(
        alert_groups=alert_groups,
        comments_by_id=comments_by_id,
        contexts_by_id=contexts_by_id,
        investigations_by_id=investigations_by_id,
        created_files=created_files,
    )
    _write_common_traces(
        alert_groups=alert_groups,
        comments=comments,
        contexts=contexts,
        investigations=investigations,
        final_summary=final_summary,
        monitoring_rows=monitoring_rows,
        created_files=created_files,
    )

    print(f"Created {len(created_files)} offline LLM IO trace files:")
    for path in sorted(created_files):
        print(path.as_posix())


if __name__ == "__main__":
    main()
