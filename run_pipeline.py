from pathlib import Path

from src.detect_anomalies import detect_anomalies
from src.generate_demo_data import generate_demo_data
from src.group_alerts import group_alerts
from src.utils import ensure_directory, save_json


RUN_ID = "demo_run"
OUTPUT_DIR = Path("outputs") / "runs" / RUN_ID


def run_pipeline() -> None:
    ensure_directory(OUTPUT_DIR)

    monitoring_data = generate_demo_data(
        output_path=OUTPUT_DIR / "monitoring_data.csv"
    )
    raw_alerts = detect_anomalies(monitoring_data)
    alert_objects, alert_groups = group_alerts(raw_alerts)

    save_json(alert_objects, OUTPUT_DIR / "alert_objects.json")
    save_json(alert_groups, OUTPUT_DIR / "alert_groups.json")

    critical_groups = sum(
        group["critical_count"] > 0 for group in alert_groups
    )
    warning_groups = sum(
        group["critical_count"] == 0 and group["warning_count"] > 0
        for group in alert_groups
    )
    expected_groups = sum(
        bool(group["is_expected_event"]) for group in alert_groups
    )

    print(f"Monitoring data rows: {len(monitoring_data)}")
    print(f"Alert objects: {len(alert_objects)}")
    print(f"Alert groups: {len(alert_groups)}")
    print(f"Critical groups: {critical_groups}")
    print(f"Warning groups: {warning_groups}")
    print(f"Expected-event groups: {expected_groups}")
    print(f"Output folder: {OUTPUT_DIR.as_posix()}/")


if __name__ == "__main__":
    run_pipeline()

