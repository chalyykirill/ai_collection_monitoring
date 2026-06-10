import json
from pathlib import Path

import pandas as pd

from src.charts import build_charts_for_alert_group
from src.report_builder import build_human_report


RUN_DIR = Path("outputs/runs/demo_run")
CHARTS_DIR = RUN_DIR / "charts"
REPORT_PATH = RUN_DIR / "human_report.html"


def _load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise ValueError(f"Expected a JSON list in {path}.")
    return value


def main() -> None:
    monitoring_df = pd.read_csv(
        RUN_DIR / "monitoring_data.csv",
        parse_dates=["report_date"],
    )
    alert_objects = _load_json(RUN_DIR / "alert_objects.json")
    alert_groups = _load_json(RUN_DIR / "alert_groups.json")
    comments = _load_json(RUN_DIR / "alert_group_comments.json")
    retrieved_contexts = _load_json(RUN_DIR / "retrieved_contexts.json")

    charts_by_group: dict[str, list[str]] = {}
    for alert_group in alert_groups:
        group_id = alert_group["alert_group_id"]
        print(f"Building charts: {group_id}")
        charts_by_group[group_id] = build_charts_for_alert_group(
            monitoring_df=monitoring_df,
            alert_group=alert_group,
            output_dir=CHARTS_DIR,
        )

    build_human_report(
        monitoring_df=monitoring_df,
        alert_objects=alert_objects,
        alert_groups=alert_groups,
        alert_group_comments=comments,
        retrieved_contexts=retrieved_contexts,
        charts_by_group=charts_by_group,
        output_path=REPORT_PATH,
    )
    print(f"Report saved: {REPORT_PATH.as_posix()}")


if __name__ == "__main__":
    main()
