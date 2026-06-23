# Investigation Planner

## Alert group

`model_gini_drop` / `alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop`

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
[Источник: model_monitoring/model_quality.md; relevance=0.0907]
# Качество модели

Событие `model_gini_drop` означает существенное снижение `gini`. Оно не является
ожидаемым и классифицируется как `potential_incident` до завершения диагностики.

Падение Gini может быть связано с изменением target rate, состава потока,
распределения score или качества признаков, 

[Источник: common/metrics_dictionary.md; relevance=0.0158]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[Источник: common/known_events.md; relevance=0.0065]
# Известные события мониторинга

## bank_unavailable_day

Единый день недоступности банка (ЕДН) является плановым технологическим
событием, если дата подтверждена календарем работ и во входных данных установлен
признак `is_expected_event=true`.

В день ЕДН допустимы нулевые `cnt_clients`, `cnt_score

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
    "alert_group_id": "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop",
    "process": "model_monitoring",
    "product": "credit_card",
    "dpd_bucket": "31-60",
    "segment": "base",
    "model_name": "collection_score_v1",
    "optimizer_name": "all",
    "event_type": "model_gini_drop",
    "main_business_zone": "model_quality",
    "main_alert": {
      "alert_id": "gini_drop_model_monitoring_credit_card_2026-05-08_0006",
      "report_id": "demo_run",
      "process": "model_monitoring",
      "block": "Model quality monitoring",
      "metric": "gini",
      "alert_type": "gini_drop",
      "product": "credit_card",
      "dpd_bucket": "31-60",
      "segment": "base",
      "model_name": "collection_score_v1",
      "model_version": "1.0",
      "optimizer_name": "all",
      "current_date": "2026-05-08",
      "previous_date": "2026-05-07",
      "current_period": "2026-05-08",
      "previous_period": "2026-05-07",
      "current_value": 0.31,
      "previous_value": 0.4261,
      "delta_abs": -0.1161,
      "delta_pp": -11.61,
      "delta_rel": -0.272471,
      "threshold_abs": 0.07,
      "severity": "critical",
      "cnt_clients": 9273,
      "event_type": "model_gini_drop",
      "is_expected_event": false,
      "is_expected_event_candidate": false,
      "python_description": "Метрика Gini изменилась с 0.4261 до 0.31; зафиксирован алерт critical.",
      "business_zone": "model_quality",
      "severity_weight": 3.0,
      "metric_weight": 1.0,
      "deviation_strength": 1.6586,
      "volume_weight": 9.135,
      "priority_score": 45.4538
    },
    "related_alerts": [
      {
        "alert_id": "target_rate_shift_model_monitoring_credit_card_2026-05-08_0007",
        "report_id": "demo_run",
        "process": "model_monitoring",
        "block": "Model quality monitoring",
        "metric": "target_rate",
        "alert_type": "target_rate_shift",
        "product": "credit_card",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-08",
        "previous_date": "2026-05-07",
        "current_period": "2026-05-08",
        "previous_period": "2026-05-07",
        "current_value": 0.225,
        "previous_value": 0.1723,
        "delta_abs": 0.0527,
        "delta_pp": 5.27,
        "delta_rel": 0.305862,
        "threshold_abs": 0.05,
        "severity": "critical",
        "cnt_clients": 9273,
        "event_type": "model_gini_drop",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Метрика target_rate изменилась с 0.1723 до 0.225; зафиксирован алерт critical.",
        "business_zone": "target_behavior",
        "severity_weight": 3.0,
        "metric_weight": 0.85,
        "deviation_strength": 1.054,
        "volume_weight": 9.135,
        "priority_score": 24.5521
      },
      {
        "alert_id": "psi_score_growth_model_monitoring_credit_card_2026-05-08_0008",
        "report_id": "demo_run",
        "process": "model_monitoring",
        "block": "Model quality monitoring",
        "metric": "psi_score",
        "alert_type": "psi_score_growth",
        "product": "credit_card",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-08",
        "previous_date": "2026-05-07",
        "current_period": "2026-05-08",
        "previous_period": "2026-05-07",
        "current_value": 0.18,
        "previous_value": 0.0304,
        "delta_abs": 0.1496,
        "delta_pp": 14.96,
        "delta_rel": 4.921053,
        "threshold_abs": 0.1,
        "severity": "warning",
        "cnt_clients": 9273,
        "event_type": "model_gini_drop",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Метрика psi_score изменилась с 0.0304 до 0.18; зафиксирован алерт warning.",
        "business_zone": "drift",
        "severity_weight": 2.0,
        "metric_weight": 0.8,
        "deviation_strength": 1.496,
        "volume_weight": 9.135,
        "priority_score": 21.8655
      }
    ],
    "group_priority_score": 91.8714,
    "alerts_count": 3,
    "critical_count": 2,
    "warning_count": 1,
    "info_count": 0,
    "metrics": [
      "gini",
      "psi_score",
      "target_rate"
    ],
    "business_zones": [
      "drift",
      "model_quality",
      "target_behavior"
    ],
    "is_expected_event": false
  },
  "alert_comment": {
    "alert_group_id": "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop",
    "short_title": "Снижение качества ранжирования модели",
    "short_conclusion": "Заметно снизилось качество ранжирования модели.",
    "facts": [
      "Gini упал с 0.4261 до 0.31.",
      "Снижение Gini составило 0.1161 и превысило порог значимого падения 0.07."
    ],
    "business_interpretation": "Модель стала менее эффективно разделять рискованные и безопасные клиенты.",
    "possible_causes": [
      "Изменение целевой ставки или состава клиентской базы.",
      "Распределение скоринга изменилось.",
      "Качество признаков ухудшилось."
    ],
    "recommended_checks": [
      "Провести углубленный анализ изменений в составе клиентской базы.",
      "Оценить распределение скоринга и его стабильность.",
      "Проверить качество и полноту используемых признаков."
    ],
    "event_classification": "potential_incident",
    "risk_level": "medium",
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
  "alert_group_id": "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop",
  "selected_tools": [
    {
      "tool_name": "check_target_rate_shift",
      "reason": "проверить изменение target_rate между текущим и предыдущим периодом",
      "expected_evidence": "изменение target_rate"
    },
    {
      "tool_name": "check_psi_shift",
      "reason": "оценить изменения psi_score и psi_features",
      "expected_evidence": "изменения psi_score и psi_features"
    },
    {
      "tool_name": "check_score_distribution_shift",
      "reason": "проверить сдвиги avg_score, median_score, p90_score и high_risk_share",
      "expected_evidence": "сдвиги в распределении scores"
    }
  ],
  "stop_reason": "выбран минимальный необходимый набор инструментов для диагностики model_gini_drop"
}
```
