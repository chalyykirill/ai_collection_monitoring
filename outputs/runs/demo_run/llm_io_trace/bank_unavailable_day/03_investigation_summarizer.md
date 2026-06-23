# Investigation Summarizer

## Alert group

`bank_unavailable_day` / `alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day`

## What this stage does

Интерпретация результатов diagnostic tools и формирование root cause hypothesis.

## Reconstruction note

Текущий builder получает `tool_results`; отдельный `tool_plan` не входит в его сигнатуру. Названия фактически выполненных tools присутствуют внутри каждого tool result.

## Model input: rendered prompt

```text
# Роль
Ты Investigation Summarizer, аналитик результатов диагностического расследования Collection.

# Цель
Свести результаты Python tools в evidence и сформировать проверяемую гипотезу root cause.

# Контекст
Опирайся только на tool_results. Не превращай исходный alert или документацию в подтвержденное evidence без результата tool. Если результаты отсутствуют, противоречивы или недостаточны, установи needs_manual_review=true и снизь confidence. Учитывай event_classification из alert_comment. Для expected_event и expected_process_feature критический статус отдельной метрики может быть механическим результатом порога и не означает инцидент, если ожидаемое событие подтверждено.
Используй только переданные входные данные и документацию. Не придумывай факты, причины, результаты проверок или положения документации. Отделяй наблюдаемые факты от гипотез. Если данных недостаточно, используй needs_manual_review там, где это допускает схема. Проведи внутренний анализ, но не показывай ход рассуждений.

# Контекст документации
[Источник: common/metrics_dictionary.md; relevance=0.0416]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[Источник: common/known_events.md; relevance=0.038]
# Известные события мониторинга

## bank_unavailable_day

Единый день недоступности банка (ЕДН) является плановым технологическим
событием, если дата подтверждена календарем работ и во входных данных установлен
признак `is_expected_event=true`.

В день ЕДН допустимы нулевые `cnt_clients`, `cnt_score

[Источник: process_monitoring/high_risk_segment.md; relevance=0.0077]
# Новый рискованный сегмент

Событие `new_high_risk_segment` не является заранее ожидаемым. Одновременный рост
`avg_score`, `median_score`, `p90_score`, `high_risk_share`, `target_rate` и
`psi_score` может указывать на изменение состава входящего потока.

До диагностики событие следует считать `pote

# Language policy
Все человекочитаемые текстовые поля верни строго на русском языке.
Не используй английские предложения.
Не используй транслитерацию.
Технические названия метрик, функций, JSON-полей и event_type можно оставлять как есть.
Примеры допустимых технических терминов: target_rate, psi_score, reject_share, check_psi_shift, model_gini_drop.
Ответ должен быть валидным JSON.

# Входные данные
{
  "alert_group": {
    "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
    "process": "process_monitoring",
    "product": "cash_loan",
    "dpd_bucket": "31-60",
    "segment": "regular_flow",
    "model_name": "all",
    "optimizer_name": "all",
    "event_type": "bank_unavailable_day",
    "main_business_zone": "volume",
    "main_alert": {
      "alert_id": "volume_drop_process_monitoring_cash_loan_2026-04-21_0001",
      "report_id": "demo_run",
      "process": "process_monitoring",
      "block": "Process monitoring",
      "metric": "cnt_clients",
      "alert_type": "volume_drop",
      "product": "cash_loan",
      "dpd_bucket": "31-60",
      "segment": "regular_flow",
      "model_name": "all",
      "model_version": "all",
      "optimizer_name": "all",
      "current_date": "2026-04-21",
      "previous_date": "2026-04-20",
      "current_period": "2026-04-21",
      "previous_period": "2026-04-20",
      "current_value": 0.0,
      "previous_value": 12245.0,
      "delta_abs": -12245.0,
      "delta_pp": -1224500.0,
      "delta_rel": -1.0,
      "threshold_abs": 0.5,
      "severity": "critical",
      "cnt_clients": 0,
      "event_type": "bank_unavailable_day",
      "is_expected_event": true,
      "is_expected_event_candidate": true,
      "python_description": "Количество клиентов изменилось с 12245 до 0; зафиксирован алерт critical.",
      "business_zone": "volume",
      "severity_weight": 3.0,
      "metric_weight": 0.85,
      "deviation_strength": 2.0,
      "volume_weight": 0.6931,
      "priority_score": 3.5351
    },
    "related_alerts": [
      {
        "alert_id": "null_metrics_spike_process_monitoring_cash_loan_2026-04-21_0002",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "null_metrics_rate",
        "alert_type": "null_metrics_spike",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "regular_flow",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-04-21",
        "previous_date": "2026-04-20",
        "current_period": "2026-04-21",
        "previous_period": "2026-04-20",
        "current_value": 0.6,
        "previous_value": 0.0,
        "delta_abs": 0.6,
        "delta_pp": 60.0,
        "delta_rel": null,
        "threshold_abs": 0.5,
        "severity": "critical",
        "cnt_clients": 0,
        "event_type": "bank_unavailable_day",
        "is_expected_event": true,
        "is_expected_event_candidate": true,
        "python_description": "Доля незаполненных ключевых метрик изменилась с 0 до 0.6; зафиксирован алерт critical.",
        "business_zone": "technical_availability",
        "severity_weight": 3.0,
        "metric_weight": 0.9,
        "deviation_strength": 1.2,
        "volume_weight": 0.6931,
        "priority_score": 2.2458
      }
    ],
    "group_priority_score": 5.7809,
    "alerts_count": 2,
    "critical_count": 2,
    "warning_count": 0,
    "info_count": 0,
    "metrics": [
      "cnt_clients",
      "null_metrics_rate"
    ],
    "business_zones": [
      "technical_availability",
      "volume"
    ],
    "is_expected_event": true
  },
  "alert_comment": {
    "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
    "short_title": "Подтвержденный ЕДН для cash loan",
    "short_conclusion": "Отклонение соответствует ожидаемому событию.",
    "facts": [
      "Объем клиентов упал до нуля.",
      "Алерты зафиксированы в business zone volume.",
      "Алерты зафиксированы в technical availability zone.",
      "Событие bank unavailable day подтверждено как ожидаемое."
    ],
    "business_interpretation": "Наблюдаемое снижение объема клиентов является запланированным техническим событием.",
    "possible_causes": [
      "Плановый единый день недоступности банка."
    ],
    "recommended_checks": [
      "Провести проверку восстановления потока на следующий рабочий день.",
      "Исключить день ЕДН из стандартного анализа динамики."
    ],
    "event_classification": "expected_event",
    "risk_level": "low",
    "confidence": "high"
  },
  "tool_results": [
    {
      "tool_name": "check_known_event_calendar",
      "status": "ok",
      "finding": "Известное событие bank_unavailable_day подтверждено признаком is_expected_event=true.",
      "evidence": {
        "event_type": "bank_unavailable_day",
        "is_expected_event": true,
        "known_expected_event_type": true,
        "event_date": "2026-04-21"
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_volume_shift",
      "status": "critical",
      "finding": "Метрики объема имеют общий статус critical.",
      "evidence": {
        "cnt_clients": {
          "current": 0.0,
          "previous": 12245.0,
          "delta_abs": -12245.0,
          "delta_rel": -1.0
        },
        "cnt_scored": {
          "current": 0.0,
          "previous": 11687.0,
          "delta_abs": -11687.0,
          "delta_rel": -1.0
        }
      },
      "supports_hypothesis": true
    }
  ]
}

# Выходные данные
evidence_summary должен перечислять только наблюдения из tool_results. root_cause_hypothesis должна оставаться гипотезой. Для expected_event и expected_process_feature не используй формулировки «потенциальная проблема», «инцидент», «сбой» или «ошибка» как трактовку события. recommended_actions должны быть контрольными: проверить завершение ожидаемого процесса и восстановление метрик, без аварийной эскалации. Для credit_card_batch_inflow объясни скачок объема и доли credit_card ожидаемым пакетным поступлением портфеля; рекомендуй контроль завершения загрузки и анализ метрик с учетом продуктового микса. Для bank_unavailable_day явно укажи, что критичное отклонение объема объяснено подтвержденным ЕДН и не является инцидентом. Для model_gini_drop threshold_abs означает порог величины падения: сравнивай abs(delta_abs) с threshold_abs и не утверждай, что текущее значение Gini ниже самого threshold_abs.
Верни строго один JSON-объект без markdown-блоков, комментариев и текста вокруг JSON.

# Выходная JSON schema
{
  "additionalProperties": false,
  "properties": {
    "alert_group_id": {
      "title": "Alert Group Id",
      "type": "string"
    },
    "evidence_summary": {
      "items": {
        "type": "string"
      },
      "title": "Evidence Summary",
      "type": "array"
    },
    "root_cause_hypothesis": {
      "title": "Root Cause Hypothesis",
      "type": "string"
    },
    "confidence": {
      "enum": [
        "low",
        "medium",
        "high"
      ],
      "title": "Confidence",
      "type": "string"
    },
    "recommended_actions": {
      "items": {
        "type": "string"
      },
      "title": "Recommended Actions",
      "type": "array"
    },
    "needs_manual_review": {
      "title": "Needs Manual Review",
      "type": "boolean"
    }
  },
  "required": [
    "alert_group_id",
    "evidence_summary",
    "root_cause_hypothesis",
    "confidence",
    "recommended_actions",
    "needs_manual_review"
  ],
  "title": "InvestigationReport",
  "type": "object"
}
```

## Model output: saved JSON

```json
{
  "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
  "evidence_summary": [
    "Событие bank_unavailable_day подтверждено признаком is_expected_event=true.",
    "Объем клиентов упал до нуля.",
    "Метрики объема имеют общий статус critical."
  ],
  "root_cause_hypothesis": "Критичное отклонение объема объяснено подтвержденным ЕДН и не является инцидентом.",
  "confidence": "high",
  "recommended_actions": [
    "Контролировать восстановление потока после завершения ЕДН."
  ],
  "needs_manual_review": false
}
```
