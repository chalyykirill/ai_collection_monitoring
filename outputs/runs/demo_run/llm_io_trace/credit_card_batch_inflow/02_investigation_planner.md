# Investigation Planner

## Alert group

`credit_card_batch_inflow` / `alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow`

## What this stage does

Выбор diagnostic tools из whitelist для расследования alert group.

## Model input: rendered prompt

```text
# Роль
Ты Investigation Planner, планировщик диагностического расследования мониторинга Collection.

# Цель
Выбрать минимальный набор Python diagnostic tools, который позволит проверить гипотезы по alert group.

# Контекст
Выбирай только инструменты из available_tools, не более пяти. Не вызывай инструменты и не придумывай их результаты. Для ожидаемого события сначала выбирай проверку календаря или известного события. Если документация уже подтверждает событие, допустим минимальный набор tools. Если подходящих tools нет, верни пустой selected_tools и объясни stop_reason. Ориентиры: для bank_unavailable_day сначала проверь календарь и объем; для credit_card_batch_inflow — календарь, продуктовый микс и при необходимости target rate; для model_gini_drop — target rate, PSI и распределение score; для empty_feature_vector — missing rate, пустые vectors и score distribution; для new_high_risk_segment — score distribution, target rate, PSI и product mix; для optimizer_mass_reject — reject share, communication mix и volume. Считай эти наборы рекомендуемым baseline: включай перечисленные tools, если они доступны в whitelist. Для bank_unavailable_day baseline обязательно включает check_known_event_calendar и check_volume_shift. Для optimizer_mass_reject baseline включает check_optimizer_reject_share, check_communication_mix_shift и check_volume_shift. Отклоняйся от baseline только если tool недоступен или явно нерелевантен, и укажи причину в stop_reason. Для expected_event выбирай не более двух tools. Для expected_process_feature выбирай не более трех tools: calendar, основную проверку особенности процесса и при необходимости одну связанную метрику. Не выбирай check_known_event_calendar для potential_incident. Не добавляй tools сверх baseline только для заполнения лимита.
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
  "available_tools": [
    {
      "tool_name": "check_known_event_calendar",
      "description": "Проверяет event_type и is_expected_event на дату события. Используется в первую очередь для bank_unavailable_day и credit_card_batch_inflow."
    },
    {
      "tool_name": "check_product_mix_shift",
      "description": "Рассчитывает долю продукта в общем объеме process_monitoring и сравнивает текущую и предыдущую даты."
    },
    {
      "tool_name": "check_target_rate_shift",
      "description": "Проверяет изменение target_rate между текущим и предыдущим периодом для среза alert group."
    },
    {
      "tool_name": "check_psi_shift",
      "description": "Проверяет изменения psi_score и psi_features относительно порогов warning и critical."
    },
    {
      "tool_name": "check_missing_rate_growth",
      "description": "Проверяет рост feature_missing_rate и score_missing_rate."
    },
    {
      "tool_name": "check_empty_feature_vector_growth",
      "description": "Проверяет рост empty_feature_vector_share."
    },
    {
      "tool_name": "check_score_distribution_shift",
      "description": "Проверяет сдвиги avg_score, median_score, p90_score и high_risk_share."
    },
    {
      "tool_name": "check_optimizer_reject_share",
      "description": "Проверяет reject_share и объемы одобренных и отклоненных решений оптимизатора."
    },
    {
      "tool_name": "check_communication_mix_shift",
      "description": "Проверяет доли каналов коммуникаций и unknown_communication_share."
    },
    {
      "tool_name": "check_volume_shift",
      "description": "Проверяет относительные изменения cnt_clients и cnt_scored."
    }
  ]
}

# Выходные данные
Для каждого выбранного инструмента объясни причину выбора и какое evidence ожидается. tool_name должен точно совпадать с именем в whitelist.
Верни строго один JSON-объект без markdown-блоков, комментариев и текста вокруг JSON.

# Выходная JSON schema
{
  "$defs": {
    "InvestigationToolCall": {
      "additionalProperties": false,
      "properties": {
        "tool_name": {
          "title": "Tool Name",
          "type": "string"
        },
        "reason": {
          "title": "Reason",
          "type": "string"
        },
        "expected_evidence": {
          "title": "Expected Evidence",
          "type": "string"
        }
      },
      "required": [
        "tool_name",
        "reason",
        "expected_evidence"
      ],
      "title": "InvestigationToolCall",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "alert_group_id": {
      "title": "Alert Group Id",
      "type": "string"
    },
    "selected_tools": {
      "items": {
        "$ref": "#/$defs/InvestigationToolCall"
      },
      "maxItems": 5,
      "title": "Selected Tools",
      "type": "array"
    },
    "stop_reason": {
      "title": "Stop Reason",
      "type": "string"
    }
  },
  "required": [
    "alert_group_id",
    "selected_tools",
    "stop_reason"
  ],
  "title": "InvestigationToolPlan",
  "type": "object"
}
```

## Model output: saved JSON

```json
{
  "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
  "selected_tools": [
    {
      "tool_name": "check_product_mix_shift",
      "reason": "проверить изменение доли продукта после ожидаемого события credit_card_batch_inflow",
      "expected_evidence": "изменение доли product_share после события"
    },
    {
      "tool_name": "check_target_rate_shift",
      "reason": "оценить влияние ожидаемого события на целевую ставку",
      "expected_evidence": "изменения целевой ставки target_rate"
    },
    {
      "tool_name": "check_volume_shift",
      "reason": "проверить общие изменения объема после ожидаемого события",
      "expected_evidence": "относительное изменение cnt_clients и cnt_scored"
    }
  ],
  "stop_reason": "выбран минимальный набор инструментов, соответствующих ожидаемому событию"
}
```
