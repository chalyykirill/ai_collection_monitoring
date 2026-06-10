import json
from pathlib import Path

from src.doc_context import get_event_doc_context
from src.llm_client import GigaChatClient
from src.prompts import ALERT_COMMENTATOR_EXAMPLES
from src.rag import retrieve_context


ALERT_GROUPS_PATH = Path("outputs/runs/demo_run/alert_groups.json")
COMMENTS_PATH = Path("outputs/runs/demo_run/alert_group_comments.json")
RETRIEVED_CONTEXTS_PATH = Path("outputs/runs/demo_run/retrieved_contexts.json")
DOCS_DIR = Path("docs")


def main() -> None:
    with ALERT_GROUPS_PATH.open(encoding="utf-8") as file:
        alert_groups = json.load(file)

    if not alert_groups:
        raise ValueError(f"No alert groups found in {ALERT_GROUPS_PATH}.")

    client = GigaChatClient()
    comments: list[dict] = []
    retrieved_contexts: list[dict] = []

    for index, alert_group in enumerate(alert_groups, start=1):
        event_type = alert_group.get("event_type", "normal")
        print(
            f"[{index}/{len(alert_groups)}] Commenting "
            f"{alert_group['alert_group_id']}"
        )
        rag_result = retrieve_context(
            alert_group=alert_group,
            docs_dir=DOCS_DIR,
        )
        doc_context = (
            rag_result["context_text"]
            or get_event_doc_context(event_type)
        )
        comment = client.comment_alert_group(
            alert_group=alert_group,
            doc_context=doc_context,
            examples=ALERT_COMMENTATOR_EXAMPLES,
        )
        comments.append(comment.model_dump())
        retrieved_contexts.append(
            {
                "alert_group_id": alert_group["alert_group_id"],
                "query": rag_result["query"],
                "chunks": [
                    {
                        "source": chunk["source"],
                        "score": chunk["score"],
                        "text_preview": chunk["text"][:300],
                    }
                    for chunk in rag_result["chunks"]
                ],
            }
        )

    COMMENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COMMENTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(comments, file, ensure_ascii=False, indent=2)
    with RETRIEVED_CONTEXTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(retrieved_contexts, file, ensure_ascii=False, indent=2)

    print(f"Comments saved: {COMMENTS_PATH.as_posix()}")
    print(f"RAG contexts saved: {RETRIEVED_CONTEXTS_PATH.as_posix()}")


if __name__ == "__main__":
    main()
