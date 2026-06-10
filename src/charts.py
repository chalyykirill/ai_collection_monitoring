from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "collection_monitoring_matplotlib"),
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


EVENT_CHARTS: dict[str, list[tuple[list[str], str]]] = {
    "bank_unavailable_day": [
        (["cnt_clients", "cnt_scored"], "Объем клиентов и скоринга"),
    ],
    "credit_card_batch_inflow": [
        (["cnt_clients"], "Объем клиентов credit_card"),
    ],
    "model_gini_drop": [
        (["gini"], "Gini модели"),
    ],
    "empty_feature_vector": [
        (
            ["empty_feature_vector_share", "feature_missing_rate"],
            "Доли пропусков в feature vector",
        ),
        (["avg_score"], "Средний score"),
    ],
    "new_high_risk_segment": [
        (["avg_score"], "Средний score"),
        (["high_risk_share", "target_rate"], "Доли риска и target"),
    ],
    "optimizer_mass_reject": [
        (["reject_share"], "Доля отказов оптимизатора"),
        (
            [
                "cnt_approved_for_communication",
                "cnt_rejected_by_optimizer",
            ],
            "Решения оптимизатора по коммуникациям",
        ),
    ],
}


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")


def _filter_group_rows(
    monitoring_df: pd.DataFrame,
    alert_group: dict[str, Any],
) -> pd.DataFrame:
    data = monitoring_df.copy()
    data["report_date"] = pd.to_datetime(data["report_date"])

    for column in (
        "process",
        "product",
        "dpd_bucket",
        "segment",
        "model_name",
        "optimizer_name",
    ):
        value = alert_group.get(column)
        if value and value != "all" and column in data.columns:
            data = data[data[column] == value]

    return data.sort_values("report_date")


def _save_line_chart(
    data: pd.DataFrame,
    metrics: list[str],
    title: str,
    event_date: pd.Timestamp,
    path: Path,
) -> bool:
    available_metrics = [
        metric
        for metric in metrics
        if metric in data.columns and data[metric].notna().any()
    ]
    if data.empty or not available_metrics:
        return False

    figure, axis = plt.subplots(figsize=(10, 4.6))
    for metric in available_metrics:
        axis.plot(
            data["report_date"],
            data[metric],
            marker="o",
            markersize=2.5,
            linewidth=1.6,
            label=metric,
        )

    axis.axvline(
        event_date,
        color="#d62728",
        linestyle="--",
        linewidth=1.5,
        label=f"событие: {event_date.date().isoformat()}",
    )
    axis.set_title(title)
    axis.set_xlabel("Дата отчета")
    axis.grid(alpha=0.25)
    axis.legend(loc="best")
    axis.xaxis.set_major_locator(mdates.AutoDateLocator())
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(figure)
    return True


def _build_credit_card_share_chart(
    monitoring_df: pd.DataFrame,
    alert_group: dict[str, Any],
    output_path: Path,
) -> bool:
    data = monitoring_df.copy()
    data["report_date"] = pd.to_datetime(data["report_date"])
    data = data[data["process"] == "process_monitoring"]
    if data.empty:
        return False

    product_volume = (
        data.groupby(["report_date", "product"], as_index=False)["cnt_clients"]
        .sum()
    )
    total_volume = (
        product_volume.groupby("report_date", as_index=False)["cnt_clients"]
        .sum()
        .rename(columns={"cnt_clients": "total_clients"})
    )
    card_volume = product_volume[
        product_volume["product"] == "credit_card"
    ].rename(columns={"cnt_clients": "credit_card_clients"})
    share = card_volume.merge(total_volume, on="report_date", how="left")
    share["credit_card_share"] = (
        share["credit_card_clients"] / share["total_clients"].replace(0, pd.NA)
    )
    event_date = pd.Timestamp(alert_group["main_alert"]["current_date"])
    return _save_line_chart(
        share,
        ["credit_card_share"],
        "Доля credit_card в потоке процесса",
        event_date,
        output_path,
    )


def build_charts_for_alert_group(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
    output_dir: Path,
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    event_type = str(alert_group.get("event_type", "unknown"))
    group_id = _safe_name(str(alert_group["alert_group_id"]))
    event_date = pd.Timestamp(alert_group["main_alert"]["current_date"])
    group_data = _filter_group_rows(monitoring_df, alert_group)
    chart_paths: list[str] = []

    chart_specs = EVENT_CHARTS.get(
        event_type,
        [([str(alert_group["main_alert"]["metric"])], "Основная метрика алерта")],
    )
    for index, (metrics, title) in enumerate(chart_specs, start=1):
        filename = f"{group_id}_{index}.png"
        path = output_dir / filename
        if _save_line_chart(group_data, metrics, title, event_date, path):
            chart_paths.append(filename)

    if event_type == "credit_card_batch_inflow":
        filename = f"{group_id}_product_share.png"
        path = output_dir / filename
        if _build_credit_card_share_chart(
            monitoring_df,
            alert_group,
            path,
        ):
            chart_paths.append(filename)

    return chart_paths
