from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pandas as pd


ToolFunction = Callable[[pd.DataFrame, dict], dict]

CHANNEL_METRICS = [
    "communication_call_share",
    "communication_visit_share",
    "communication_sms_share",
    "communication_waiting_share",
    "communication_agency_share",
    "unknown_communication_share",
]

TOOL_DESCRIPTIONS = {
    "check_known_event_calendar": (
        "Проверяет event_type и is_expected_event на дату события. "
        "Используется в первую очередь для bank_unavailable_day и "
        "credit_card_batch_inflow."
    ),
    "check_product_mix_shift": (
        "Рассчитывает долю продукта в общем объеме process_monitoring и "
        "сравнивает текущую и предыдущую даты."
    ),
    "check_target_rate_shift": (
        "Проверяет изменение target_rate между текущим и предыдущим периодом "
        "для среза alert group."
    ),
    "check_psi_shift": (
        "Проверяет изменения psi_score и psi_features относительно порогов "
        "warning и critical."
    ),
    "check_missing_rate_growth": (
        "Проверяет рост feature_missing_rate и score_missing_rate."
    ),
    "check_empty_feature_vector_growth": (
        "Проверяет рост empty_feature_vector_share."
    ),
    "check_score_distribution_shift": (
        "Проверяет сдвиги avg_score, median_score, p90_score и "
        "high_risk_share."
    ),
    "check_optimizer_reject_share": (
        "Проверяет reject_share и объемы одобренных и отклоненных решений "
        "оптимизатора."
    ),
    "check_communication_mix_shift": (
        "Проверяет доли каналов коммуникаций и "
        "unknown_communication_share."
    ),
    "check_volume_shift": (
        "Проверяет относительные изменения cnt_clients и cnt_scored."
    ),
}


def _value(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    return round(float(value), 6)


def _relative_delta(current: float, previous: float) -> float | None:
    if previous == 0:
        return None
    return round((current - previous) / abs(previous), 6)


def _status(
    deviation: float,
    warning_threshold: float,
    critical_threshold: float,
) -> str:
    if deviation >= critical_threshold:
        return "critical"
    if deviation >= warning_threshold:
        return "warning"
    return "ok"


def _max_status(statuses: list[str]) -> str:
    order = {"ok": 0, "warning": 1, "critical": 2}
    return max(statuses, key=order.get) if statuses else "ok"


def _group_rows(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> tuple[pd.Series | None, pd.Series | None]:
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

    main_alert = alert_group["main_alert"]
    current_date = pd.Timestamp(main_alert["current_date"])
    previous_date = pd.Timestamp(main_alert["previous_date"])
    current_rows = data[data["report_date"] == current_date]
    previous_rows = data[data["report_date"] == previous_date]
    current = None if current_rows.empty else current_rows.iloc[0]
    previous = None if previous_rows.empty else previous_rows.iloc[0]
    return current, previous


def _missing_rows_result(tool_name: str) -> dict:
    return {
        "tool_name": tool_name,
        "status": "warning",
        "finding": "Текущий или предыдущий срез мониторинга не найден.",
        "evidence": {},
        "supports_hypothesis": False,
    }


def _metric_evidence(
    current: pd.Series,
    previous: pd.Series,
    metric: str,
) -> dict[str, Any]:
    current_value = _value(current.get(metric))
    previous_value = _value(previous.get(metric))
    if current_value is None or previous_value is None:
        return {
            "current": current_value,
            "previous": previous_value,
            "delta_abs": None,
            "delta_rel": None,
        }
    return {
        "current": current_value,
        "previous": previous_value,
        "delta_abs": round(current_value - previous_value, 6),
        "delta_rel": _relative_delta(current_value, previous_value),
    }


def check_known_event_calendar(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_known_event_calendar"
    current, _ = _group_rows(monitoring_df, alert_group)
    if current is None:
        return _missing_rows_result(tool_name)

    event_type = str(current.get("event_type", alert_group.get("event_type")))
    expected_flag = bool(current.get("is_expected_event", False))
    known_expected = event_type in {
        "bank_unavailable_day",
        "credit_card_batch_inflow",
    }
    confirmed = known_expected and expected_flag
    return {
        "tool_name": tool_name,
        "status": "ok" if confirmed else "warning",
        "finding": (
            f"Известное событие {event_type} подтверждено признаком "
            "is_expected_event=true."
            if confirmed
            else (
                f"Для события {event_type} отсутствует подтверждение "
                "признаком is_expected_event=true."
            )
        ),
        "evidence": {
            "event_type": event_type,
            "is_expected_event": expected_flag,
            "known_expected_event_type": known_expected,
            "event_date": str(alert_group["main_alert"]["current_date"]),
        },
        "supports_hypothesis": confirmed,
    }


def check_product_mix_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_product_mix_shift"
    data = monitoring_df.copy()
    data["report_date"] = pd.to_datetime(data["report_date"])
    data = data[data["process"] == "process_monitoring"]
    product = str(alert_group.get("product", "all"))
    current_date = pd.Timestamp(alert_group["main_alert"]["current_date"])
    previous_date = pd.Timestamp(alert_group["main_alert"]["previous_date"])

    def product_share(report_date: pd.Timestamp) -> tuple[float | None, int, int]:
        daily = data[data["report_date"] == report_date]
        total = int(daily["cnt_clients"].sum())
        product_count = int(
            daily.loc[daily["product"] == product, "cnt_clients"].sum()
        )
        share = None if total == 0 else product_count / total
        return share, product_count, total

    current_share, current_count, current_total = product_share(current_date)
    previous_share, previous_count, previous_total = product_share(previous_date)
    if current_share is None or previous_share is None:
        return _missing_rows_result(tool_name)

    delta = current_share - previous_share
    status = _status(abs(delta), 0.10, 0.20)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": (
            f"Доля продукта {product} изменилась на "
            f"{delta * 100:.2f} п.п."
        ),
        "evidence": {
            "product": product,
            "current_share": round(current_share, 6),
            "previous_share": round(previous_share, 6),
            "delta_pp": round(delta * 100, 4),
            "current_product_clients": current_count,
            "previous_product_clients": previous_count,
            "current_total_clients": current_total,
            "previous_total_clients": previous_total,
        },
        "supports_hypothesis": status != "ok",
    }


def check_target_rate_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_target_rate_shift"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)
    evidence = _metric_evidence(current, previous, "target_rate")
    delta = evidence["delta_abs"]
    if delta is None:
        return _missing_rows_result(tool_name)
    status = _status(abs(delta), 0.02, 0.05)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"target_rate изменился на {delta * 100:.2f} п.п.",
        "evidence": evidence,
        "supports_hypothesis": status != "ok",
    }


def check_psi_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_psi_shift"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    metrics: dict[str, Any] = {}
    statuses: list[str] = []
    for metric in ("psi_score", "psi_features"):
        evidence = _metric_evidence(current, previous, metric)
        metrics[metric] = evidence
        delta = evidence["delta_abs"]
        if delta is not None:
            statuses.append(_status(max(delta, 0), 0.10, 0.20))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"PSI-метрики имеют общий статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


def check_missing_rate_growth(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_missing_rate_growth"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    thresholds = {
        "feature_missing_rate": (0.10, 0.25),
        "score_missing_rate": (0.05, 0.15),
    }
    metrics: dict[str, Any] = {}
    statuses: list[str] = []
    for metric, (warning, critical) in thresholds.items():
        evidence = _metric_evidence(current, previous, metric)
        metrics[metric] = evidence
        delta = evidence["delta_abs"]
        if delta is not None:
            statuses.append(_status(max(delta, 0), warning, critical))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"Метрики пропусков имеют общий статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


def check_empty_feature_vector_growth(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_empty_feature_vector_growth"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)
    evidence = _metric_evidence(
        current,
        previous,
        "empty_feature_vector_share",
    )
    delta = evidence["delta_abs"]
    if delta is None:
        return _missing_rows_result(tool_name)
    status = _status(max(delta, 0), 0.02, 0.05)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": (
            "empty_feature_vector_share изменился на "
            f"{delta * 100:.2f} п.п."
        ),
        "evidence": evidence,
        "supports_hypothesis": status != "ok",
    }


def check_score_distribution_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_score_distribution_shift"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    metrics: dict[str, Any] = {}
    statuses: list[str] = []
    for metric in (
        "avg_score",
        "median_score",
        "p90_score",
        "high_risk_share",
    ):
        evidence = _metric_evidence(current, previous, metric)
        metrics[metric] = evidence
        delta = evidence["delta_abs"]
        if delta is not None:
            statuses.append(_status(abs(delta), 0.05, 0.10))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"Распределение score имеет общий статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


def check_optimizer_reject_share(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_optimizer_reject_share"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    metrics = {
        metric: _metric_evidence(current, previous, metric)
        for metric in (
            "reject_share",
            "cnt_approved_for_communication",
            "cnt_rejected_by_optimizer",
        )
    }
    statuses: list[str] = []
    reject_delta = metrics["reject_share"]["delta_abs"]
    if reject_delta is not None:
        statuses.append(_status(max(reject_delta, 0), 0.10, 0.25))
    approved_delta = metrics["cnt_approved_for_communication"]["delta_rel"]
    if approved_delta is not None:
        statuses.append(_status(max(-approved_delta, 0), 0.20, 0.50))
    rejected_delta = metrics["cnt_rejected_by_optimizer"]["delta_rel"]
    if rejected_delta is not None:
        statuses.append(_status(max(rejected_delta, 0), 0.30, 0.70))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"Метрики отказов оптимизатора имеют статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


def check_communication_mix_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_communication_mix_shift"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    metrics: dict[str, Any] = {}
    statuses: list[str] = []
    for metric in CHANNEL_METRICS:
        evidence = _metric_evidence(current, previous, metric)
        metrics[metric] = evidence
        delta = evidence["delta_abs"]
        if delta is None:
            continue
        thresholds = (0.05, 0.15) if metric == "unknown_communication_share" else (0.10, 0.25)
        statuses.append(_status(abs(delta), *thresholds))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"Микс коммуникаций имеет общий статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


def check_volume_shift(
    monitoring_df: pd.DataFrame,
    alert_group: dict,
) -> dict:
    tool_name = "check_volume_shift"
    current, previous = _group_rows(monitoring_df, alert_group)
    if current is None or previous is None:
        return _missing_rows_result(tool_name)

    metrics = {
        metric: _metric_evidence(current, previous, metric)
        for metric in ("cnt_clients", "cnt_scored")
    }
    statuses: list[str] = []
    for evidence in metrics.values():
        delta_rel = evidence["delta_rel"]
        if delta_rel is None:
            continue
        if delta_rel < 0:
            statuses.append(_status(abs(delta_rel), 0.20, 0.50))
        else:
            statuses.append(_status(delta_rel, 0.30, 0.70))
    status = _max_status(statuses)
    return {
        "tool_name": tool_name,
        "status": status,
        "finding": f"Метрики объема имеют общий статус {status}.",
        "evidence": metrics,
        "supports_hypothesis": status != "ok",
    }


TOOL_REGISTRY: dict[str, ToolFunction] = {
    "check_known_event_calendar": check_known_event_calendar,
    "check_product_mix_shift": check_product_mix_shift,
    "check_target_rate_shift": check_target_rate_shift,
    "check_psi_shift": check_psi_shift,
    "check_missing_rate_growth": check_missing_rate_growth,
    "check_empty_feature_vector_growth": check_empty_feature_vector_growth,
    "check_score_distribution_shift": check_score_distribution_shift,
    "check_optimizer_reject_share": check_optimizer_reject_share,
    "check_communication_mix_shift": check_communication_mix_shift,
    "check_volume_shift": check_volume_shift,
}


def get_available_tools() -> list[dict[str, str]]:
    return [
        {"tool_name": name, "description": TOOL_DESCRIPTIONS[name]}
        for name in TOOL_REGISTRY
    ]
