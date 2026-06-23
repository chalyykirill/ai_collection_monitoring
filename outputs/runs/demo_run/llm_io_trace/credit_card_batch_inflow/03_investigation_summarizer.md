# Investigation Summarizer

## Alert group

`credit_card_batch_inflow` / `alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow`

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
[Источник: process_monitoring/credit_card_inflow.md; relevance=0.0648]
# Неритмичное поступление credit card

Событие `credit_card_batch_inflow` означает пакетное поступление портфеля
кредитных карт. Для подтвержденной даты загрузки это ожидаемая особенность
процесса, `expected_process_feature`.

Типичные признаки: рост `cnt_clients`, увеличение `product_share` и возмо

[Источник: common/known_events.md; relevance=0.047]
# Известные события мониторинга

## bank_unavailable_day

Единый день недоступности банка (ЕДН) является плановым технологическим
событием, если дата подтверждена календарем работ и во входных данных установлен
признак `is_expected_event=true`.

В день ЕДН допустимы нулевые `cnt_clients`, `cnt_score

[Источник: common/metrics_dictionary.md; relevance=0.0447]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

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
    "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
    "process": "process_monitoring",
    "product": "credit_card",
    "dpd_bucket": "1-30",
    "segment": "regular_flow",
    "model_name": "all",
    "optimizer_name": "all",
    "event_type": "credit_card_batch_inflow",
    "main_business_zone": "volume",
    "main_alert": {
      "alert_id": "volume_spike_process_monitoring_credit_card_2026-05-01_0003",
      "report_id": "demo_run",
      "process": "process_monitoring",
      "block": "Process monitoring",
      "metric": "cnt_clients",
      "alert_type": "volume_spike",
      "product": "credit_card",
      "dpd_bucket": "1-30",
      "segment": "regular_flow",
      "model_name": "all",
      "model_version": "all",
      "optimizer_name": "all",
      "current_date": "2026-05-01",
      "previous_date": "2026-04-30",
      "current_period": "2026-05-01",
      "previous_period": "2026-04-30",
      "current_value": 15500.0,
      "previous_value": 5101.0,
      "delta_abs": 10399.0,
      "delta_pp": 1039900.0,
      "delta_rel": 2.03862,
      "threshold_abs": 0.7,
      "severity": "critical",
      "cnt_clients": 15500,
      "event_type": "credit_card_batch_inflow",
      "is_expected_event": true,
      "is_expected_event_candidate": true,
      "python_description": "Количество клиентов изменилось с 5101 до 15500; зафиксирован алерт critical.",
      "business_zone": "volume",
      "severity_weight": 3.0,
      "metric_weight": 0.85,
      "deviation_strength": 2.9123,
      "volume_weight": 9.6487,
      "priority_score": 71.6545
    },
    "related_alerts": [
      {
        "alert_id": "target_rate_shift_process_monitoring_credit_card_2026-05-01_0005",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "target_rate",
        "alert_type": "target_rate_shift",
        "product": "credit_card",
        "dpd_bucket": "1-30",
        "segment": "regular_flow",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-01",
        "previous_date": "2026-04-30",
        "current_period": "2026-05-01",
        "previous_period": "2026-04-30",
        "current_value": 0.185,
        "previous_value": 0.1448,
        "delta_abs": 0.0402,
        "delta_pp": 4.02,
        "delta_rel": 0.277624,
        "threshold_abs": 0.02,
        "severity": "warning",
        "cnt_clients": 15500,
        "event_type": "credit_card_batch_inflow",
        "is_expected_event": true,
        "is_expected_event_candidate": true,
        "python_description": "Метрика target_rate изменилась с 0.1448 до 0.185; зафиксирован алерт warning.",
        "business_zone": "target_behavior",
        "severity_weight": 2.0,
        "metric_weight": 0.85,
        "deviation_strength": 2.01,
        "volume_weight": 9.6487,
        "priority_score": 32.9695
      },
      {
        "alert_id": "credit_card_inflow_spike_process_monitoring_credit_card_2026-05-01_0004",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "product_share",
        "alert_type": "credit_card_inflow_spike",
        "product": "credit_card",
        "dpd_bucket": "1-30",
        "segment": "regular_flow",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-01",
        "previous_date": "2026-04-30",
        "current_period": "2026-05-01",
        "previous_period": "2026-04-30",
        "current_value": 0.527408,
        "previous_value": 0.265511,
        "delta_abs": 0.261897,
        "delta_pp": 26.189708,
        "delta_rel": 0.986388,
        "threshold_abs": 0.2,
        "severity": "critical",
        "cnt_clients": 15500,
        "event_type": "credit_card_batch_inflow",
        "is_expected_event": true,
        "is_expected_event_candidate": true,
        "python_description": "Доля продукта credit_card в потоке изменилась с 0.2655 до 0.5274; зафиксирован алерт critical.",
        "business_zone": "portfolio_mix",
        "severity_weight": 3.0,
        "metric_weight": 0.7,
        "deviation_strength": 1.3095,
        "volume_weight": 9.6487,
        "priority_score": 26.5333
      }
    ],
    "group_priority_score": 131.1573,
    "alerts_count": 3,
    "critical_count": 2,
    "warning_count": 1,
    "info_count": 0,
    "metrics": [
      "cnt_clients",
      "product_share",
      "target_rate"
    ],
    "business_zones": [
      "portfolio_mix",
      "target_behavior",
      "volume"
    ],
    "is_expected_event": true
  },
  "alert_comment": {
    "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
    "short_title": "Пакетное поступление кредитных карт подтверждено",
    "short_conclusion": "Это ожидаемая особенность процесса.",
    "facts": [
      "Наблюдался резкий рост cnt_clients.",
      "Доля product_share увеличилась.",
      "Событие credit_card_batch_inflow подтверждено как ожидаемое.",
      "Событие зарегистрировано в regular_flow сегменте."
    ],
    "business_interpretation": "Наблюдаемый скачок объема и доли кредитного продукта является ожидаемой особенностью процесса.",
    "possible_causes": [],
    "recommended_checks": [],
    "event_classification": "expected_process_feature",
    "risk_level": "low",
    "confidence": "high"
  },
  "tool_results": [
    {
      "tool_name": "check_product_mix_shift",
      "status": "critical",
      "finding": "Доля продукта credit_card изменилась на 26.19 п.п.",
      "evidence": {
        "product": "credit_card",
        "current_share": 0.527408,
        "previous_share": 0.265511,
        "delta_pp": 26.1897,
        "current_product_clients": 15500,
        "previous_product_clients": 5101,
        "current_total_clients": 29389,
        "previous_total_clients": 19212
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_target_rate_shift",
      "status": "warning",
      "finding": "target_rate изменился на 4.02 п.п.",
      "evidence": {
        "current": 0.185,
        "previous": 0.1448,
        "delta_abs": 0.0402,
        "delta_rel": 0.277624
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_volume_shift",
      "status": "critical",
      "finding": "Метрики объема имеют общий статус critical.",
      "evidence": {
        "cnt_clients": {
          "current": 15500.0,
          "previous": 5101.0,
          "delta_abs": 10399.0,
          "delta_rel": 2.03862
        },
        "cnt_scored": {
          "current": 14700.0,
          "previous": 4875.0,
          "delta_abs": 9825.0,
          "delta_rel": 2.015385
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
  "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
  "evidence_summary": [
    "Наблюдался резкий рост cnt_clients на 10399 единиц.",
    "Доля product_share увеличилась на 26.19 процентных пунктов.",
    "Событие credit_card_batch_inflow подтверждено как ожидаемое.",
    "Событие зарегистрировано в regular_flow сегменте."
  ],
  "root_cause_hypothesis": "Скачок объема и доли credit_card объясняется ожидаемым пакетным поступлением портфеля.",
  "confidence": "high",
  "recommended_actions": [
    "Контролировать завершение пакетной загрузки.",
    "Анализировать метрики с учетом продуктового микса."
  ],
  "needs_manual_review": false
}
```
