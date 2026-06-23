# Investigation Planner

## Alert group

`bank_unavailable_day` / `alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day`

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
  "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
  "selected_tools": [
    {
      "tool_name": "check_known_event_calendar",
      "reason": "Подтвердить, что bank_unavailable_day является ожидаемым событием согласно календарю работ",
      "expected_evidence": "Дата bank_unavailable_day присутствует в known events calendar"
    },
    {
      "tool_name": "check_volume_shift",
      "reason": "Оценить относительное изменение cnt_clients и cnt_scored за период bank_unavailable_day",
      "expected_evidence": "Относительное изменение cnt_clients и cnt_scored находится в пределах нормы для запланированного технического события"
    }
  ],
  "stop_reason": ""
}
```
