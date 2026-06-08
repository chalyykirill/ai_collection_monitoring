from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.utils import ensure_directory


COLUMNS = [
    "report_date",
    "report_month",
    "process",
    "product",
    "dpd_bucket",
    "segment",
    "model_name",
    "model_version",
    "optimizer_name",
    "cnt_clients",
    "cnt_scored",
    "cnt_approved_for_communication",
    "cnt_rejected_by_optimizer",
    "reject_share",
    "target_rate",
    "gini",
    "avg_score",
    "median_score",
    "p90_score",
    "high_risk_share",
    "score_missing_rate",
    "feature_missing_rate",
    "empty_feature_vector_share",
    "psi_score",
    "psi_features",
    "communication_call_share",
    "communication_visit_share",
    "communication_sms_share",
    "communication_waiting_share",
    "communication_agency_share",
    "unknown_communication_share",
    "event_type",
    "is_expected_event",
]


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return round(float(np.clip(value, low, high)), 4)


def _base_row(
    report_date: pd.Timestamp,
    process: str,
    product: str,
    dpd_bucket: str,
    segment: str,
    **values: Any,
) -> dict[str, Any]:
    row = {column: np.nan for column in COLUMNS}
    row.update(
        {
            "report_date": report_date.strftime("%Y-%m-%d"),
            "report_month": report_date.strftime("%Y-%m"),
            "process": process,
            "product": product,
            "dpd_bucket": dpd_bucket,
            "segment": segment,
            "model_name": "all",
            "model_version": "all",
            "optimizer_name": "all",
            "event_type": "normal",
            "is_expected_event": False,
        }
    )
    row.update(values)
    return row


def _process_rows(
    report_date: pd.Timestamp,
    rng: np.random.Generator,
) -> list[dict[str, Any]]:
    cash_clients = max(1, int(rng.normal(12_000, 260)))
    card_clients = max(1, int(rng.normal(5_200, 180)))
    risk_clients = max(1, int(rng.normal(1_800, 90)))

    return [
        _base_row(
            report_date,
            "process_monitoring",
            "cash_loan",
            "31-60",
            "regular_flow",
            cnt_clients=cash_clients,
            cnt_scored=int(cash_clients * rng.normal(0.96, 0.004)),
            target_rate=_clip(rng.normal(0.18, 0.004)),
            avg_score=_clip(rng.normal(0.49, 0.008)),
            median_score=_clip(rng.normal(0.48, 0.008)),
            p90_score=_clip(rng.normal(0.72, 0.008)),
            high_risk_share=_clip(rng.normal(0.19, 0.006)),
            score_missing_rate=_clip(rng.normal(0.008, 0.0015)),
            feature_missing_rate=_clip(rng.normal(0.018, 0.002)),
            empty_feature_vector_share=_clip(rng.normal(0.002, 0.0005)),
            psi_score=_clip(rng.normal(0.035, 0.005)),
            psi_features=_clip(rng.normal(0.04, 0.005)),
        ),
        _base_row(
            report_date,
            "process_monitoring",
            "credit_card",
            "1-30",
            "regular_flow",
            cnt_clients=card_clients,
            cnt_scored=int(card_clients * rng.normal(0.95, 0.005)),
            target_rate=_clip(rng.normal(0.14, 0.004)),
            avg_score=_clip(rng.normal(0.46, 0.008)),
            median_score=_clip(rng.normal(0.45, 0.008)),
            p90_score=_clip(rng.normal(0.69, 0.009)),
            high_risk_share=_clip(rng.normal(0.15, 0.005)),
            score_missing_rate=_clip(rng.normal(0.009, 0.0015)),
            feature_missing_rate=_clip(rng.normal(0.02, 0.002)),
            empty_feature_vector_share=_clip(rng.normal(0.003, 0.0006)),
            psi_score=_clip(rng.normal(0.04, 0.005)),
            psi_features=_clip(rng.normal(0.045, 0.005)),
        ),
        _base_row(
            report_date,
            "process_monitoring",
            "cash_loan",
            "61-90",
            "new_high_risk",
            cnt_clients=risk_clients,
            cnt_scored=int(risk_clients * rng.normal(0.95, 0.006)),
            target_rate=_clip(rng.normal(0.24, 0.005)),
            avg_score=_clip(rng.normal(0.56, 0.008)),
            median_score=_clip(rng.normal(0.55, 0.008)),
            p90_score=_clip(rng.normal(0.78, 0.009)),
            high_risk_share=_clip(rng.normal(0.22, 0.006)),
            score_missing_rate=_clip(rng.normal(0.01, 0.0015)),
            feature_missing_rate=_clip(rng.normal(0.022, 0.002)),
            empty_feature_vector_share=_clip(rng.normal(0.003, 0.0006)),
            psi_score=_clip(rng.normal(0.04, 0.005)),
            psi_features=_clip(rng.normal(0.045, 0.005)),
        ),
    ]


def _model_row(
    report_date: pd.Timestamp,
    rng: np.random.Generator,
) -> dict[str, Any]:
    clients = max(1, int(rng.normal(9_500, 180)))
    return _base_row(
        report_date,
        "model_monitoring",
        "credit_card",
        "31-60",
        "base",
        model_name="collection_score_v1",
        model_version="1.0",
        cnt_clients=clients,
        cnt_scored=int(clients * rng.normal(0.98, 0.003)),
        target_rate=_clip(rng.normal(0.17, 0.004)),
        gini=_clip(rng.normal(0.43, 0.006)),
        avg_score=_clip(rng.normal(0.51, 0.007)),
        median_score=_clip(rng.normal(0.50, 0.007)),
        p90_score=_clip(rng.normal(0.75, 0.008)),
        high_risk_share=_clip(rng.normal(0.20, 0.005)),
        score_missing_rate=_clip(rng.normal(0.006, 0.001)),
        feature_missing_rate=_clip(rng.normal(0.015, 0.002)),
        empty_feature_vector_share=_clip(rng.normal(0.002, 0.0004)),
        psi_score=_clip(rng.normal(0.04, 0.005)),
        psi_features=_clip(rng.normal(0.045, 0.005)),
    )


def _data_quality_row(
    report_date: pd.Timestamp,
    rng: np.random.Generator,
) -> dict[str, Any]:
    clients = max(1, int(rng.normal(9_000, 170)))
    return _base_row(
        report_date,
        "data_quality_monitoring",
        "cash_loan",
        "31-60",
        "base",
        model_name="collection_score_v1",
        model_version="1.0",
        cnt_clients=clients,
        cnt_scored=int(clients * rng.normal(0.97, 0.004)),
        avg_score=_clip(rng.normal(0.50, 0.007)),
        median_score=_clip(rng.normal(0.49, 0.007)),
        p90_score=_clip(rng.normal(0.73, 0.008)),
        score_missing_rate=_clip(rng.normal(0.01, 0.002)),
        feature_missing_rate=_clip(rng.normal(0.02, 0.003)),
        empty_feature_vector_share=_clip(rng.normal(0.003, 0.0007)),
        psi_score=_clip(rng.normal(0.035, 0.005)),
        psi_features=_clip(rng.normal(0.04, 0.006)),
        unknown_communication_share=_clip(rng.normal(0.005, 0.001)),
    )


def _optimizer_row(
    report_date: pd.Timestamp,
    rng: np.random.Generator,
) -> dict[str, Any]:
    clients = max(1, int(rng.normal(11_000, 220)))
    rejected = max(0, int(clients * rng.normal(0.20, 0.008)))
    approved = max(0, int(clients * rng.normal(0.68, 0.01)))
    return _base_row(
        report_date,
        "optimizer_monitoring",
        "cash_loan",
        "31-60",
        "regular_flow",
        optimizer_name="collection_contact_optimizer",
        cnt_clients=clients,
        cnt_approved_for_communication=approved,
        cnt_rejected_by_optimizer=rejected,
        reject_share=_clip(rejected / clients),
        communication_call_share=_clip(rng.normal(0.30, 0.008)),
        communication_visit_share=_clip(rng.normal(0.16, 0.006)),
        communication_sms_share=_clip(rng.normal(0.25, 0.008)),
        communication_waiting_share=_clip(rng.normal(0.14, 0.006)),
        communication_agency_share=_clip(rng.normal(0.10, 0.005)),
        unknown_communication_share=_clip(rng.normal(0.01, 0.002)),
    )


def _apply_demo_events(data: pd.DataFrame, dates: pd.DatetimeIndex) -> None:
    event_dates = {
        "bank_unavailable_day": dates[24].strftime("%Y-%m-%d"),
        "credit_card_batch_inflow": dates[34].strftime("%Y-%m-%d"),
        "model_gini_drop": dates[41].strftime("%Y-%m-%d"),
        "empty_feature_vector": dates[47].strftime("%Y-%m-%d"),
        "new_high_risk_segment": dates[53].strftime("%Y-%m-%d"),
        "optimizer_mass_reject": dates[59].strftime("%Y-%m-%d"),
    }

    edn = (
        (data["report_date"] == event_dates["bank_unavailable_day"])
        & (data["process"] == "process_monitoring")
        & (data["product"] == "cash_loan")
        & (data["segment"] == "regular_flow")
    )
    data.loc[edn, ["cnt_clients", "cnt_scored"]] = 0
    data.loc[
        edn,
        [
            "target_rate",
            "avg_score",
            "median_score",
            "p90_score",
            "high_risk_share",
            "score_missing_rate",
            "feature_missing_rate",
            "empty_feature_vector_share",
            "psi_score",
            "psi_features",
        ],
    ] = np.nan
    data.loc[edn, ["event_type", "is_expected_event"]] = [
        "bank_unavailable_day",
        True,
    ]

    card_batch = (
        (data["report_date"] == event_dates["credit_card_batch_inflow"])
        & (data["process"] == "process_monitoring")
        & (data["product"] == "credit_card")
    )
    data.loc[card_batch, "cnt_clients"] = 15_500
    data.loc[card_batch, "cnt_scored"] = 14_700
    data.loc[card_batch, "target_rate"] = 0.185
    data.loc[card_batch, ["event_type", "is_expected_event"]] = [
        "credit_card_batch_inflow",
        True,
    ]

    gini_drop = (
        (data["report_date"] == event_dates["model_gini_drop"])
        & (data["process"] == "model_monitoring")
    )
    data.loc[gini_drop, ["gini", "target_rate", "psi_score"]] = [0.31, 0.225, 0.18]
    data.loc[gini_drop, "event_type"] = "model_gini_drop"

    empty_vector = (
        (data["report_date"] == event_dates["empty_feature_vector"])
        & (data["process"] == "data_quality_monitoring")
    )
    data.loc[
        empty_vector,
        [
            "feature_missing_rate",
            "empty_feature_vector_share",
            "score_missing_rate",
            "avg_score",
            "median_score",
            "p90_score",
            "psi_features",
        ],
    ] = [0.38, 0.11, 0.19, 0.68, 0.67, 0.88, 0.29]
    data.loc[empty_vector, "event_type"] = "empty_feature_vector"

    risk_segment = (
        (data["report_date"] == event_dates["new_high_risk_segment"])
        & (data["process"] == "process_monitoring")
        & (data["segment"] == "new_high_risk")
    )
    data.loc[
        risk_segment,
        [
            "cnt_clients",
            "cnt_scored",
            "target_rate",
            "avg_score",
            "median_score",
            "p90_score",
            "high_risk_share",
            "psi_score",
        ],
    ] = [4_100, 3_950, 0.39, 0.74, 0.73, 0.93, 0.49, 0.28]
    data.loc[risk_segment, "event_type"] = "new_high_risk_segment"

    mass_reject = (
        (data["report_date"] == event_dates["optimizer_mass_reject"])
        & (data["process"] == "optimizer_monitoring")
    )
    data.loc[
        mass_reject,
        [
            "cnt_approved_for_communication",
            "cnt_rejected_by_optimizer",
            "reject_share",
            "communication_call_share",
            "communication_visit_share",
            "communication_sms_share",
            "communication_waiting_share",
            "communication_agency_share",
            "unknown_communication_share",
        ],
    ] = [1_350, 9_100, 0.83, 0.03, 0.02, 0.04, 0.02, 0.01, 0.18]
    data.loc[mass_reject, "event_type"] = "optimizer_mass_reject"


def generate_demo_data(
    output_path: Path | None = None,
    days: int = 65,
    seed: int = 42,
) -> pd.DataFrame:
    if days < 60:
        raise ValueError("Demo monitoring data must cover at least 60 days.")

    rng = np.random.default_rng(seed)
    dates = pd.date_range(end="2026-05-31", periods=days, freq="D")
    rows: list[dict[str, Any]] = []

    for report_date in dates:
        rows.extend(_process_rows(report_date, rng))
        rows.append(_model_row(report_date, rng))
        rows.append(_data_quality_row(report_date, rng))
        rows.append(_optimizer_row(report_date, rng))

    data = pd.DataFrame(rows, columns=COLUMNS)
    _apply_demo_events(data, dates)
    data = data.sort_values(
        ["report_date", "process", "product", "dpd_bucket", "segment"]
    ).reset_index(drop=True)

    if output_path is not None:
        ensure_directory(output_path.parent)
        data.to_csv(output_path, index=False)

    return data

