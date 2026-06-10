import json
from pathlib import Path

from src.doc_context import get_event_doc_context
from src.llm_client import GigaChatClient
from src.prompts import ALERT_COMMENTATOR_EXAMPLES


ALERT_GROUPS_PATH = Path("outputs/runs/demo_run/alert_groups.json")
COMMENT_PATH = Path("outputs/runs/demo_run/comment.json")


def main() -> None:
    with ALERT_GROUPS_PATH.open(encoding="utf-8") as file:
        alert_groups = json.load(file)

    if not alert_groups:
        raise ValueError(f"No alert groups found in {ALERT_GROUPS_PATH}.")

    first_alert_group = alert_groups[0]
    comment = GigaChatClient().comment_alert_group(
        alert_group=first_alert_group,
        doc_context=get_event_doc_context(first_alert_group["event_type"]),
        examples=ALERT_COMMENTATOR_EXAMPLES,
    )
    COMMENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COMMENT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            comment.model_dump(),
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Alert group: {first_alert_group['alert_group_id']}")
    print(f"Comment saved: {COMMENT_PATH.as_posix()}")


if __name__ == "__main__":
    main()
