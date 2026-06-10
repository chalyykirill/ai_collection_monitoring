from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd


IDENTITY_COLUMNS = [
    "process",
    "product",
    "dpd_bucket",
    "segment",
    "model_name",
    "model_version",
    "optimizer_name",
]

BLOCK_BY_PROCESS = {
    "process_monitoring": "Process monitoring",
    "model_monitoring": "Model quality monitoring",
    "optimizer_monitoring": "Optimizer monitoring",
    "data_quality_monitoring": "Data quality monitoring",
}

NULL_METRICS_BY_PROCESS = {
    "process_monitoring": [
        "cnt_clients",
        "cnt_scored",
        "target_rate",
        "avg_score",
        "high_risk_share",
    ],
    "model_monitoring": [
        "cnt_clients",
        "cnt_scored",
        "gini",
        "target_rate",
        "avg_score",
        "psi_score",
    ],
    "optimizer_monitoring": [
        "cnt_clients",
        "reject_share",
        "cnt_approved_for_communication",
        "cnt_rejected_by_optimizer",
    ],
    "data_quality_monitoring": [
        "cnt_clients",
        "cnt_scored",
        "score_missing_rate",
        "feature_missing_rate",
        "empty_feature_vector_share",
        "avg_score",
    ],
}

METRIC_LABELS = {
    "cnt_clients": "Количество клиентов",
    "null_metrics_rate": "Доля незаполненных ключевых метрик",
    "product_share": "Доля продукта credit_card в потоке",
    "gini": "Метрика Gini",
    "target_rate": "Метрика target_rate",
    "avg_score": "Средний score",
    "median_score": "Медианный score",
    "p90_score": "90-й перцентиль score",
    "high_risk_share": "Доля high-risk клиентов",
    "feature_missing_rate": "Доля пропущенных признаков",
    "empty_feature_vector_share": "Доля пустых feature vector",
    "psi_score": "Метрика psi_score",
    "psi_features": "PSI признаков",
    "reject_share": "Доля отказов оптимизатора",
    "cnt_approved_for_communication": "Количество одобренных коммуникаций",
    "unknown_communication_share": "Доля неизвестных коммуникаций",
}

METRIC_CHANGE_VERBS = {
    "cnt_clients": "изменилось",
    "null_metrics_rate": "изменилась",
    "product_share": "изменилась",
    "gini": "изменилась",
    "target_rate": "изменилась",
    "avg_score": "изменился",
    "median_score": "изменился",
    "p90_score": "изменился",
    "high_risk_share": "изменилась",
    "feature_missing_rate": "изменилась",
    "empty_feature_vector_share": "изменилась",
    "psi_score": "изменилась",
    "psi_features": "изменился",
    "reject_share": "изменилась",
    "cnt_approved_for_communication": "изменилось",
    "unknown_communication_share": "изменилась",
}


def _number(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    return float(value)


def _round(value: float | None, digits: int = 6) -> float | None:
    return None if value is None else round(float(value), digits)


def _relative_delta(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return (current - previous) / abs(previous)


def _severity(
    deviation: float,
    warning_threshold: float,
    critical_threshold: float,
) -> tuple[str | None, float | None]:
    if deviation >= critical_threshold:
        return "critical", critical_threshold
    if deviation >= warning_threshold:
        return "warning", warning_threshold
    return None, None


def _identity(row: pd.Series) -> tuple[str, ...]:
    return tuple(
        "all" if pd.isna(row[column]) else str(row[column])
        for column in IDENTITY_COLUMNS
    )


def _format_value(value: float | None) -> str:
    if value is None:
        return "NULL"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _description(
    metric: str,
    previous_value: float | None,
    current_value: float | None,
    severity: str,
) -> str:
    label = METRIC_LABELS.get(metric, metric)
    change_verb = METRIC_CHANGE_VERBS.get(metric, "изменилась")
    return (
        f"{label} {change_verb} с {_format_value(previous_value)} "
        f"до {_format_value(current_value)}; зафиксирован алерт {severity}."
    )


def _build_alert(
    alerts: list[dict[str, Any]],
    row: pd.Series,
    previous_row: pd.Series,
    metric: str,
    alert_type: str,
    current_value: float,
    previous_value: float,
    threshold_abs: float,
    severity: str,
) -> None:
    delta_abs = current_value - previous_value
    delta_rel = _relative_delta(current_value, previous_value)
    current_date = str(row["report_date"])
    previous_date = str(previous_row["report_date"])
    event_type = str(row.get("event_type", "normal"))
    expected = bool(row.get("is_expected_event", False))
    alert_number = len(alerts) + 1

    alerts.append(
        {
            "alert_id": (
                f"{alert_type}_{row['process']}_{row['product']}_"
                f"{current_date}_{alert_number:04d}"
            ),
            "report_id": "demo_run",
            "process": str(row["process"]),
            "block": BLOCK_BY_PROCESS.get(str(row["process"]), "Monitoring"),
            "metric": metric,
            "alert_type": alert_type,
            "product": str(row.get("product", "all")),
            "dpd_bucket": str(row.get("dpd_bucket", "all")),
            "segment": str(row.get("segment", "all")),
            "model_name": str(row.get("model_name", "all")),
            "model_version": str(row.get("model_version", "all")),
            "optimizer_name": str(row.get("optimizer_name", "all")),
            "current_date": current_date,
            "previous_date": previous_date,
            "current_period": current_date,
            "previous_period": previous_date,
            "current_value": _round(current_value),
            "previous_value": _round(previous_value),
            "delta_abs": _round(delta_abs),
            "delta_pp": _round(delta_abs * 100),
            "delta_rel": _round(delta_rel),
            "threshold_abs": _round(threshold_abs),
            "severity": severity,
            "cnt_clients": int(row["cnt_clients"])
            if not pd.isna(row.get("cnt_clients"))
            else 0,
            "event_type": event_type,
            "is_expected_event": expected,
            "is_expected_event_candidate": expected,
            "python_description": _description(
                metric,
                previous_value,
                current_value,
                severity,
            ),
        }
    )


def _check_delta_rule(
    alerts: list[dict[str, Any]],
    row: pd.Series,
    previous_row: pd.Series,
    metric: str,
    alert_type: str,
    warning_threshold: float,
    critical_threshold: float,
    deviation_getter: Callable[[float, float], float],
) -> None:
    current_value = _number(row.get(metric))
    previous_value = _number(previous_row.get(metric))
    if current_value is None or previous_value is None:
        return

    deviation = deviation_getter(current_value, previous_value)
    severity, threshold = _severity(
        deviation,
        warning_threshold,
        critical_threshold,
    )
    if severity is not None and threshold is not None:
        _build_alert(
            alerts,
            row,
            previous_row,
            metric,
            alert_type,
            current_value,
            previous_value,
            threshold,
            severity,
        )


def _product_share_by_date(data: pd.DataFrame) -> dict[tuple[str, str], float]:
    process_data = data[data["process"] == "process_monitoring"].copy()
    product_volume = (
        process_data.groupby(["report_date", "product"], as_index=False)["cnt_clients"]
        .sum()
        .rename(columns={"cnt_clients": "product_clients"})
    )
    total_volume = (
        process_data.groupby("report_date", as_index=False)["cnt_clients"]
        .sum()
        .rename(columns={"cnt_clients": "total_clients"})
    )
    shares = product_volume.merge(total_volume, on="report_date")
    shares["product_share"] = (
        shares["product_clients"] / shares["total_clients"].replace(0, np.nan)
    )
    return {
        (str(row.report_date), str(row.product)): float(row.product_share)
        for row in shares.itertuples()
        if not pd.isna(row.product_share)
    }


def detect_anomalies(data: pd.DataFrame) -> list[dict[str, Any]]:
    required = set(IDENTITY_COLUMNS + ["report_date", "cnt_clients"])
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Monitoring data is missing columns: {sorted(missing)}")

    working_data = data.copy()
    working_data["report_date"] = working_data["report_date"].astype(str)
    working_data = working_data.sort_values("report_date")
    product_shares = _product_share_by_date(working_data)
    bank_unavailable_dates = set(
        working_data.loc[
            working_data["event_type"] == "bank_unavailable_day",
            "report_date",
        ]
    )
    previous_by_identity: dict[tuple[str, ...], pd.Series] = {}
    alerts: list[dict[str, Any]] = []

    for _, row in working_data.iterrows():
        key = _identity(row)
        previous_row = previous_by_identity.get(key)
        previous_by_identity[key] = row
        if previous_row is None:
            continue
        if (
            str(row.get("event_type", "normal")) == "normal"
            and str(previous_row.get("event_type", "normal")) != "normal"
        ):
            # The first normal day is a recovery baseline, not a new incident.
            continue

        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "cnt_clients",
            "volume_drop",
            0.20,
            0.50,
            lambda current, previous: (
                (previous - current) / previous if previous > 0 else 0.0
            ),
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "cnt_clients",
            "volume_spike",
            0.30,
            0.70,
            lambda current, previous: (
                (current - previous) / previous if previous > 0 else 0.0
            ),
        )

        null_metrics = NULL_METRICS_BY_PROCESS.get(str(row["process"]), [])
        current_null_rate = float(row[null_metrics].isna().mean())
        previous_null_rate = float(previous_row[null_metrics].isna().mean())
        null_growth = current_null_rate - previous_null_rate
        severity, threshold = _severity(null_growth, 0.20, 0.50)
        if severity is not None and threshold is not None:
            _build_alert(
                alerts,
                row,
                previous_row,
                "null_metrics_rate",
                "null_metrics_spike",
                current_null_rate,
                previous_null_rate,
                threshold,
                severity,
            )

        if (
            row["process"] == "process_monitoring"
            and row["product"] == "credit_card"
            and row["report_date"] not in bank_unavailable_dates
        ):
            current_share = product_shares.get(
                (str(row["report_date"]), "credit_card")
            )
            previous_share = product_shares.get(
                (str(previous_row["report_date"]), "credit_card")
            )
            if current_share is not None and previous_share is not None:
                share_growth = current_share - previous_share
                severity, threshold = _severity(share_growth, 0.10, 0.20)
                if severity is not None and threshold is not None:
                    _build_alert(
                        alerts,
                        row,
                        previous_row,
                        "product_share",
                        "credit_card_inflow_spike",
                        current_share,
                        previous_share,
                        threshold,
                        severity,
                    )

        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "gini",
            "gini_drop",
            0.03,
            0.07,
            lambda current, previous: previous - current,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "target_rate",
            "target_rate_shift",
            0.02,
            0.05,
            lambda current, previous: abs(current - previous),
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "avg_score",
            "avg_score_shift",
            0.05,
            0.10,
            lambda current, previous: abs(current - previous),
        )
        for metric in ("median_score", "p90_score"):
            _check_delta_rule(
                alerts,
                row,
                previous_row,
                metric,
                "score_distribution_shift",
                0.05,
                0.10,
                lambda current, previous: abs(current - previous),
            )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "high_risk_share",
            "high_risk_share_growth",
            0.05,
            0.10,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "feature_missing_rate",
            "feature_missing_rate_growth",
            0.10,
            0.25,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "empty_feature_vector_share",
            "empty_feature_vector_growth",
            0.02,
            0.05,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "psi_score",
            "psi_score_growth",
            0.10,
            0.20,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "psi_features",
            "psi_features_growth",
            0.10,
            0.20,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "reject_share",
            "reject_share_growth",
            0.10,
            0.25,
            lambda current, previous: current - previous,
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "cnt_approved_for_communication",
            "approved_communication_drop",
            0.20,
            0.50,
            lambda current, previous: (
                (previous - current) / previous if previous > 0 else 0.0
            ),
        )
        _check_delta_rule(
            alerts,
            row,
            previous_row,
            "unknown_communication_share",
            "unknown_communication_share_growth",
            0.05,
            0.15,
            lambda current, previous: current - previous,
        )

    return alerts
