import json
from pathlib import Path

import pandas as pd

from src.investigation_agent import run_investigation_for_group
from src.llm_client import GigaChatClient


RUN_DIR = Path("outputs/runs/demo_run")
OUTPUT_PATH = RUN_DIR / "investigation_reports.json"


def _load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise ValueError(f"Expected a JSON list in {path}.")
    return value


def _rag_context(context: dict) -> str:
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


def main() -> None:
    monitoring_df = pd.read_csv(
        RUN_DIR / "monitoring_data.csv",
        parse_dates=["report_date"],
    )
    alert_groups = _load_json(RUN_DIR / "alert_groups.json")
    comments = _load_json(RUN_DIR / "alert_group_comments.json")
    retrieved_contexts = _load_json(RUN_DIR / "retrieved_contexts.json")

    comments_by_id = {
        comment["alert_group_id"]: comment
        for comment in comments
    }
    contexts_by_id = {
        context["alert_group_id"]: context
        for context in retrieved_contexts
    }
    client = GigaChatClient()
    investigations: list[dict] = []

    for index, alert_group in enumerate(alert_groups, start=1):
        group_id = alert_group["alert_group_id"]
        if group_id not in comments_by_id:
            raise ValueError(f"Comment is missing for {group_id}.")
        if group_id not in contexts_by_id:
            raise ValueError(f"RAG context is missing for {group_id}.")

        print(
            f"[{index}/{len(alert_groups)}] Investigating "
            f"{alert_group['event_type']}"
        )
        investigations.append(
            run_investigation_for_group(
                monitoring_df=monitoring_df,
                alert_group=alert_group,
                alert_comment=comments_by_id[group_id],
                rag_context=_rag_context(contexts_by_id[group_id]),
                llm_client=client,
            )
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(investigations, file, ensure_ascii=False, indent=2)

    print(f"Investigation reports saved: {OUTPUT_PATH.as_posix()}")


if __name__ == "__main__":
    main()
