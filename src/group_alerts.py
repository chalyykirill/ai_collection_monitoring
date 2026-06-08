from __future__ import annotations

import math
from collections import defaultdict
from typing import Any


METRIC_TO_BUSINESS_ZONE = {
    "cnt_clients": "volume",
    "cnt_scored": "volume",
    "product_share": "portfolio_mix",
    "null_metrics_rate": "technical_availability",
    "gini": "model_quality",
    "target_rate": "target_behavior",
    "avg_score": "score_stability",
    "median_score": "score_stability",
    "p90_score": "score_stability",
    "high_risk_share": "portfolio_risk",
    "score_missing_rate": "data_quality",
    "feature_missing_rate": "data_quality",
    "empty_feature_vector_share": "data_quality",
    "psi_score": "drift",
    "psi_features": "drift",
    "reject_share": "optimizer_behavior",
    "cnt_rejected_by_optimizer": "optimizer_behavior",
    "cnt_approved_for_communication": "optimizer_behavior",
    "unknown_communication_share": "data_quality",
}

SEVERITY_WEIGHT = {
    "info": 1.0,
    "warning": 2.0,
    "critical": 3.0,
}

METRIC_WEIGHT = {
    "gini": 1.0,
    "reject_share": 1.0,
    "empty_feature_vector_share": 0.95,
    "feature_missing_rate": 0.90,
    "cnt_approved_for_communication": 0.90,
    "null_metrics_rate": 0.90,
    "cnt_clients": 0.85,
    "target_rate": 0.85,
    "avg_score": 0.80,
    "psi_score": 0.80,
    "psi_features": 0.80,
    "high_risk_share": 0.75,
    "product_share": 0.70,
    "median_score": 0.70,
    "p90_score": 0.70,
    "unknown_communication_share": 0.65,
}

RELATIVE_ALERT_TYPES = {
    "volume_drop",
    "volume_spike",
    "approved_communication_drop",
}

GROUP_COLUMNS = [
    "process",
    "product",
    "dpd_bucket",
    "segment",
    "model_name",
    "optimizer_name",
    "event_type",
]


def _deviation_strength(alert: dict[str, Any]) -> float:
    threshold = abs(float(alert.get("threshold_abs") or 0))
    if threshold == 0:
        return 1.0

    if alert.get("alert_type") in RELATIVE_ALERT_TYPES:
        deviation = abs(float(alert.get("delta_rel") or 0))
    else:
        deviation = abs(float(alert.get("delta_abs") or 0))
    return round(max(1.0, deviation / threshold), 4)


def enrich_alert(alert: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(alert)
    severity_weight = SEVERITY_WEIGHT.get(str(alert.get("severity")), 1.0)
    metric_weight = METRIC_WEIGHT.get(str(alert.get("metric")), 0.60)
    deviation_strength = _deviation_strength(alert)
    cnt_clients = max(0, int(alert.get("cnt_clients") or 0))
    volume_weight = math.log1p(max(cnt_clients, 1))
    priority_score = (
        severity_weight
        * metric_weight
        * deviation_strength
        * volume_weight
    )

    enriched.update(
        {
            "business_zone": METRIC_TO_BUSINESS_ZONE.get(
                str(alert.get("metric")),
                "other",
            ),
            "severity_weight": severity_weight,
            "metric_weight": metric_weight,
            "deviation_strength": deviation_strength,
            "volume_weight": round(volume_weight, 4),
            "priority_score": round(priority_score, 4),
        }
    )
    return enriched


def _group_key(alert: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(alert.get(column) or "all") for column in GROUP_COLUMNS)


def _group_id(key: tuple[str, ...], index: int) -> str:
    normalized = [
        value.lower().replace(" ", "_").replace("/", "_")
        for value in key
    ]
    return f"alert_group_{index:03d}__{'__'.join(normalized)}"


def group_alerts(
    alerts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    enriched_alerts = [enrich_alert(alert) for alert in alerts]
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for alert in enriched_alerts:
        grouped[_group_key(alert)].append(alert)

    groups: list[dict[str, Any]] = []
    for index, (key, group_items) in enumerate(grouped.items(), start=1):
        sorted_items = sorted(
            group_items,
            key=lambda item: item["priority_score"],
            reverse=True,
        )
        main_alert = sorted_items[0]
        critical_count = sum(
            item["severity"] == "critical" for item in sorted_items
        )
        warning_count = sum(
            item["severity"] == "warning" for item in sorted_items
        )
        group = {
            "alert_group_id": _group_id(key, index),
            **dict(zip(GROUP_COLUMNS, key)),
            "main_business_zone": main_alert["business_zone"],
            "main_alert": main_alert,
            "related_alerts": sorted_items[1:],
            "group_priority_score": round(
                sum(item["priority_score"] for item in sorted_items),
                4,
            ),
            "alerts_count": len(sorted_items),
            "critical_count": critical_count,
            "warning_count": warning_count,
            "info_count": sum(
                item["severity"] == "info" for item in sorted_items
            ),
            "metrics": sorted({item["metric"] for item in sorted_items}),
            "business_zones": sorted(
                {item["business_zone"] for item in sorted_items}
            ),
            "is_expected_event": any(
                bool(item.get("is_expected_event")) for item in sorted_items
            ),
        }
        groups.append(group)

    groups.sort(
        key=lambda item: item["group_priority_score"],
        reverse=True,
    )
    return enriched_alerts, groups

