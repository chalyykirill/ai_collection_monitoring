# Investigation Planner

## Alert group

`optimizer_mass_reject` / `alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject`

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
[Источник: optimizer_monitoring/optimizer_rules.md; relevance=0.0727]
# Правила бизнес-оптимизатора

Событие `optimizer_mass_reject` означает массовый рост решений reject или
no action одновременно с падением `cnt_approved_for_communication`. Это не
является штатным режимом и классифицируется как `potential_incident`.

Возможные причины: изменение правил, исчерпание б

[Источник: common/metrics_dictionary.md; relevance=0.057]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[Источник: optimizer_monitoring/anomaly_playbook.md; relevance=0.0136]
# Playbook оптимизатора

При массовых отказах:

- проверить версии и условия бизнес-правил;
- проверить бюджетные и контактные ограничения;
- проверить входные признаки оптимизатора;
- проверить справочники доступных коммуникаций;
- сравнить reject share по каналам, продуктам и сегментам.

Массовое

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
    "alert_group_id": "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
    "process": "optimizer_monitoring",
    "product": "cash_loan",
    "dpd_bucket": "31-60",
    "segment": "regular_flow",
    "model_name": "all",
    "optimizer_name": "collection_contact_optimizer",
    "event_type": "optimizer_mass_reject",
    "main_business_zone": "optimizer_behavior",
    "main_alert": {
      "alert_id": "reject_share_growth_optimizer_monitoring_cash_loan_2026-05-26_0022",
      "report_id": "demo_run",
      "process": "optimizer_monitoring",
      "block": "Optimizer monitoring",
      "metric": "reject_share",
      "alert_type": "reject_share_growth",
      "product": "cash_loan",
      "dpd_bucket": "31-60",
      "segment": "regular_flow",
      "model_name": "all",
      "model_version": "all",
      "optimizer_name": "collection_contact_optimizer",
      "current_date": "2026-05-26",
      "previous_date": "2026-05-25",
      "current_period": "2026-05-26",
      "previous_period": "2026-05-25",
      "current_value": 0.83,
      "previous_value": 0.1949,
      "delta_abs": 0.6351,
      "delta_pp": 63.51,
      "delta_rel": 3.258594,
      "threshold_abs": 0.25,
      "severity": "critical",
      "cnt_clients": 10831,
      "event_type": "optimizer_mass_reject",
      "is_expected_event": false,
      "is_expected_event_candidate": false,
      "python_description": "Доля отказов оптимизатора изменилась с 0.1949 до 0.83; зафиксирован алерт critical.",
      "business_zone": "optimizer_behavior",
      "severity_weight": 3.0,
      "metric_weight": 1.0,
      "deviation_strength": 2.5404,
      "volume_weight": 9.2903,
      "priority_score": 70.8029
    },
    "related_alerts": [
      {
        "alert_id": "approved_communication_drop_optimizer_monitoring_cash_loan_2026-05-26_0023",
        "report_id": "demo_run",
        "process": "optimizer_monitoring",
        "block": "Optimizer monitoring",
        "metric": "cnt_approved_for_communication",
        "alert_type": "approved_communication_drop",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "regular_flow",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "collection_contact_optimizer",
        "current_date": "2026-05-26",
        "previous_date": "2026-05-25",
        "current_period": "2026-05-26",
        "previous_period": "2026-05-25",
        "current_value": 1350.0,
        "previous_value": 7401.0,
        "delta_abs": -6051.0,
        "delta_pp": -605100.0,
        "delta_rel": -0.817592,
        "threshold_abs": 0.5,
        "severity": "critical",
        "cnt_clients": 10831,
        "event_type": "optimizer_mass_reject",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Количество одобренных коммуникаций изменилось с 7401 до 1350; зафиксирован алерт critical.",
        "business_zone": "optimizer_behavior",
        "severity_weight": 3.0,
        "metric_weight": 0.9,
        "deviation_strength": 1.6352,
        "volume_weight": 9.2903,
        "priority_score": 41.0169
      },
      {
        "alert_id": "unknown_communication_share_growth_optimizer_monitoring_cash_loan_2026-05-26_0024",
        "report_id": "demo_run",
        "process": "optimizer_monitoring",
        "block": "Optimizer monitoring",
        "metric": "unknown_communication_share",
        "alert_type": "unknown_communication_share_growth",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "regular_flow",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "collection_contact_optimizer",
        "current_date": "2026-05-26",
        "previous_date": "2026-05-25",
        "current_period": "2026-05-26",
        "previous_period": "2026-05-25",
        "current_value": 0.18,
        "previous_value": 0.0096,
        "delta_abs": 0.1704,
        "delta_pp": 17.04,
        "delta_rel": 17.75,
        "threshold_abs": 0.15,
        "severity": "critical",
        "cnt_clients": 10831,
        "event_type": "optimizer_mass_reject",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Доля неизвестных коммуникаций изменилась с 0.0096 до 0.18; зафиксирован алерт critical.",
        "business_zone": "data_quality",
        "severity_weight": 3.0,
        "metric_weight": 0.65,
        "deviation_strength": 1.136,
        "volume_weight": 9.2903,
        "priority_score": 20.5798
      }
    ],
    "group_priority_score": 132.3996,
    "alerts_count": 3,
    "critical_count": 3,
    "warning_count": 0,
    "info_count": 0,
    "metrics": [
      "cnt_approved_for_communication",
      "reject_share",
      "unknown_communication_share"
    ],
    "business_zones": [
      "data_quality",
      "optimizer_behavior"
    ],
    "is_expected_event": false
  },
  "alert_comment": {
    "alert_group_id": "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
    "short_title": "Массовое ограничение коммуникаций оптимизатором",
    "short_conclusion": "Наблюдается потенциальный инцидент в работе оптимизатора.",
    "facts": [
      "Доля отказов оптимизатора значительно увеличилась.",
      "Количество одобренных коммуникаций резко сократилось.",
      "Доля неизвестных коммуникаций также возросла."
    ],
    "business_interpretation": "Оптимизатор чрезмерно ограничивает возможности коммуникаций, что может негативно сказаться на сборе задолженности.",
    "possible_causes": [
      "Изменения в правилах или условиях работы оптимизатора.",
      "Проблемы с доступными коммуникациями или их настройками.",
      "Недостаточный бюджет или исчерпание лимитов оптимизатора."
    ],
    "recommended_checks": [
      "Провести детальный аудит изменений в правилах и условиях оптимизатора.",
      "Проверить доступные и настроенные каналы коммуникаций.",
      "Оценить текущий бюджет и лимиты оптимизатора."
    ],
    "event_classification": "potential_incident",
    "risk_level": "high",
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
  "alert_group_id": "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
  "selected_tools": [
    {
      "tool_name": "check_optimizer_reject_share",
      "reason": "проверить reject_share и объемы одобренных и отклоненных решений оптимизатора",
      "expected_evidence": "изменение reject_share и объемов одобренных и отклоненных решений оптимизатора"
    },
    {
      "tool_name": "check_communication_mix_shift",
      "reason": "проверить доли каналов коммуникаций и unknown_communication_share",
      "expected_evidence": "изменения долей каналов коммуникаций и unknown_communication_share"
    },
    {
      "tool_name": "check_volume_shift",
      "reason": "проверить относительные изменения cnt_clients и cnt_scored",
      "expected_evidence": "относительные изменения cnt_clients и cnt_scored"
    }
  ],
  "stop_reason": "выбран минимальный набор инструментов из доступной whitelist"
}
```
