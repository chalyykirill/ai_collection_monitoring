# Investigation Planner

## Alert group

`empty_feature_vector` / `alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector`

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
[Источник: data_quality_monitoring/feature_vector_quality.md; relevance=0.0627]
# Качество feature vector

Событие `empty_feature_vector` означает рост доли пустых или частично
незаполненных входных признаков. Если alert group подтверждает превышение
порогов по `empty_feature_vector_share` или `feature_missing_rate`, само
отклонение классифицируется как `potential_incident` кач

[Источник: common/metrics_dictionary.md; relevance=0.0589]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[Источник: data_quality_monitoring/anomaly_playbook.md; relevance=0.0119]
# Playbook качества данных

При росте missing rate:

- локализовать пропуски по источникам и признакам;
- сравнить время обновления витрин;
- проверить объем пустых feature vector;
- оценить влияние пропусков на score;
- проверить восстановление после исправления загрузки.

Причину следует считать п

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
    "alert_group_id": "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
    "process": "data_quality_monitoring",
    "product": "cash_loan",
    "dpd_bucket": "31-60",
    "segment": "base",
    "model_name": "collection_score_v1",
    "optimizer_name": "all",
    "event_type": "empty_feature_vector",
    "main_business_zone": "data_quality",
    "main_alert": {
      "alert_id": "empty_feature_vector_growth_data_quality_monitoring_cash_loan_2026-05-14_0013",
      "report_id": "demo_run",
      "process": "data_quality_monitoring",
      "block": "Data quality monitoring",
      "metric": "empty_feature_vector_share",
      "alert_type": "empty_feature_vector_growth",
      "product": "cash_loan",
      "dpd_bucket": "31-60",
      "segment": "base",
      "model_name": "collection_score_v1",
      "model_version": "1.0",
      "optimizer_name": "all",
      "current_date": "2026-05-14",
      "previous_date": "2026-05-13",
      "current_period": "2026-05-14",
      "previous_period": "2026-05-13",
      "current_value": 0.11,
      "previous_value": 0.0027,
      "delta_abs": 0.1073,
      "delta_pp": 10.73,
      "delta_rel": 39.740741,
      "threshold_abs": 0.05,
      "severity": "critical",
      "cnt_clients": 8915,
      "event_type": "empty_feature_vector",
      "is_expected_event": false,
      "is_expected_event_candidate": false,
      "python_description": "Доля пустых feature vector изменилась с 0.0027 до 0.11; зафиксирован алерт critical.",
      "business_zone": "data_quality",
      "severity_weight": 3.0,
      "metric_weight": 0.95,
      "deviation_strength": 2.146,
      "volume_weight": 9.0956,
      "priority_score": 55.6296
    },
    "related_alerts": [
      {
        "alert_id": "avg_score_shift_data_quality_monitoring_cash_loan_2026-05-14_0009",
        "report_id": "demo_run",
        "process": "data_quality_monitoring",
        "block": "Data quality monitoring",
        "metric": "avg_score",
        "alert_type": "avg_score_shift",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-14",
        "previous_date": "2026-05-13",
        "current_period": "2026-05-14",
        "previous_period": "2026-05-13",
        "current_value": 0.68,
        "previous_value": 0.4959,
        "delta_abs": 0.1841,
        "delta_pp": 18.41,
        "delta_rel": 0.371244,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 8915,
        "event_type": "empty_feature_vector",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Средний score изменился с 0.4959 до 0.68; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.8,
        "deviation_strength": 1.841,
        "volume_weight": 9.0956,
        "priority_score": 40.188
      },
      {
        "alert_id": "feature_missing_rate_growth_data_quality_monitoring_cash_loan_2026-05-14_0012",
        "report_id": "demo_run",
        "process": "data_quality_monitoring",
        "block": "Data quality monitoring",
        "metric": "feature_missing_rate",
        "alert_type": "feature_missing_rate_growth",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-14",
        "previous_date": "2026-05-13",
        "current_period": "2026-05-14",
        "previous_period": "2026-05-13",
        "current_value": 0.38,
        "previous_value": 0.0156,
        "delta_abs": 0.3644,
        "delta_pp": 36.44,
        "delta_rel": 23.358974,
        "threshold_abs": 0.25,
        "severity": "critical",
        "cnt_clients": 8915,
        "event_type": "empty_feature_vector",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Доля пропущенных признаков изменилась с 0.0156 до 0.38; зафиксирован алерт critical.",
        "business_zone": "data_quality",
        "severity_weight": 3.0,
        "metric_weight": 0.9,
        "deviation_strength": 1.4576,
        "volume_weight": 9.0956,
        "priority_score": 35.7959
      },
      {
        "alert_id": "score_distribution_shift_data_quality_monitoring_cash_loan_2026-05-14_0010",
        "report_id": "demo_run",
        "process": "data_quality_monitoring",
        "block": "Data quality monitoring",
        "metric": "median_score",
        "alert_type": "score_distribution_shift",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-14",
        "previous_date": "2026-05-13",
        "current_period": "2026-05-14",
        "previous_period": "2026-05-13",
        "current_value": 0.67,
        "previous_value": 0.4836,
        "delta_abs": 0.1864,
        "delta_pp": 18.64,
        "delta_rel": 0.385443,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 8915,
        "event_type": "empty_feature_vector",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Медианный score изменился с 0.4836 до 0.67; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.7,
        "deviation_strength": 1.864,
        "volume_weight": 9.0956,
        "priority_score": 35.6038
      },
      {
        "alert_id": "score_distribution_shift_data_quality_monitoring_cash_loan_2026-05-14_0011",
        "report_id": "demo_run",
        "process": "data_quality_monitoring",
        "block": "Data quality monitoring",
        "metric": "p90_score",
        "alert_type": "score_distribution_shift",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-14",
        "previous_date": "2026-05-13",
        "current_period": "2026-05-14",
        "previous_period": "2026-05-13",
        "current_value": 0.88,
        "previous_value": 0.7295,
        "delta_abs": 0.1505,
        "delta_pp": 15.05,
        "delta_rel": 0.206306,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 8915,
        "event_type": "empty_feature_vector",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "90-й перцентиль score изменился с 0.7295 до 0.88; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.7,
        "deviation_strength": 1.505,
        "volume_weight": 9.0956,
        "priority_score": 28.7467
      },
      {
        "alert_id": "psi_features_growth_data_quality_monitoring_cash_loan_2026-05-14_0014",
        "report_id": "demo_run",
        "process": "data_quality_monitoring",
        "block": "Data quality monitoring",
        "metric": "psi_features",
        "alert_type": "psi_features_growth",
        "product": "cash_loan",
        "dpd_bucket": "31-60",
        "segment": "base",
        "model_name": "collection_score_v1",
        "model_version": "1.0",
        "optimizer_name": "all",
        "current_date": "2026-05-14",
        "previous_date": "2026-05-13",
        "current_period": "2026-05-14",
        "previous_period": "2026-05-13",
        "current_value": 0.29,
        "previous_value": 0.0335,
        "delta_abs": 0.2565,
        "delta_pp": 25.65,
        "delta_rel": 7.656716,
        "threshold_abs": 0.2,
        "severity": "critical",
        "cnt_clients": 8915,
        "event_type": "empty_feature_vector",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "PSI признаков изменился с 0.0335 до 0.29; зафиксирован алерт critical.",
        "business_zone": "drift",
        "severity_weight": 3.0,
        "metric_weight": 0.8,
        "deviation_strength": 1.2825,
        "volume_weight": 9.0956,
        "priority_score": 27.9963
      }
    ],
    "group_priority_score": 223.9603,
    "alerts_count": 6,
    "critical_count": 6,
    "warning_count": 0,
    "info_count": 0,
    "metrics": [
      "avg_score",
      "empty_feature_vector_share",
      "feature_missing_rate",
      "median_score",
      "p90_score",
      "psi_features"
    ],
    "business_zones": [
      "data_quality",
      "drift",
      "score_stability"
    ],
    "is_expected_event": false
  },
  "alert_comment": {
    "alert_group_id": "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
    "short_title": "Рост доли пустых feature vector",
    "short_conclusion": "Наблюдается значительное увеличение доли пустых feature vector.",
    "facts": [
      "Доля пустых feature vector увеличилась с 0.0027 до 0.11.",
      "Это изменение превышает установленный порог и классифицируется как критическое."
    ],
    "business_interpretation": "Увеличение доли пустых feature vector может повлиять на точность моделей и качество прогнозов.",
    "possible_causes": [
      "Проблемы с качеством исходных данных или их загрузкой.",
      "Технологические сбои в процессе обработки данных."
    ],
    "recommended_checks": [
      "Провести детальный анализ качества источников данных и процессов их загрузки.",
      "Оценить влияние увеличения доли пустых feature vector на ключевые показатели моделей."
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
  "alert_group_id": "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
  "selected_tools": [
    {
      "tool_name": "check_empty_feature_vector_growth",
      "reason": "Проверка роста доли пустых feature vector, так как это ключевое событие alert group",
      "expected_evidence": "Подтверждение роста доли пустых feature vector"
    },
    {
      "tool_name": "check_missing_rate_growth",
      "reason": "Анализ роста feature_missing_rate для оценки общего качества данных",
      "expected_evidence": "Подтверждение роста feature_missing_rate"
    },
    {
      "tool_name": "check_score_distribution_shift",
      "reason": "Оценка изменений в распределении scores для выявления влияния пустых feature vector",
      "expected_evidence": "Изменения в avg_score, median_score, p90_score и high_risk_share"
    }
  ],
  "stop_reason": ""
}
```
