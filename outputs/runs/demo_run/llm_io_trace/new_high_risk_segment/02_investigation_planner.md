# Investigation Planner

## Alert group

`new_high_risk_segment` / `alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment`

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
[Источник: process_monitoring/high_risk_segment.md; relevance=0.0682]
# Новый рискованный сегмент

Событие `new_high_risk_segment` не является заранее ожидаемым. Одновременный рост
`avg_score`, `median_score`, `p90_score`, `high_risk_share`, `target_rate` и
`psi_score` может указывать на изменение состава входящего потока.

До диагностики событие следует считать `pote

[Источник: common/metrics_dictionary.md; relevance=0.0565]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[Источник: process_monitoring/anomaly_playbook.md; relevance=0.0131]
# Playbook мониторинга процесса

При скачке объема проверьте календарь известных событий, источник загрузки и
изменение продуктового состава.

При одновременном сдвиге риска и объема сравните текущий поток с предыдущим
периодом по `product`, `dpd_bucket` и `segment`. Не интерпретируйте рост score ка

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
    "alert_group_id": "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
    "process": "process_monitoring",
    "product": "cash_loan",
    "dpd_bucket": "61-90",
    "segment": "new_high_risk",
    "model_name": "all",
    "optimizer_name": "all",
    "event_type": "new_high_risk_segment",
    "main_business_zone": "target_behavior",
    "main_alert": {
      "alert_id": "target_rate_shift_process_monitoring_cash_loan_2026-05-20_0016",
      "report_id": "demo_run",
      "process": "process_monitoring",
      "block": "Process monitoring",
      "metric": "target_rate",
      "alert_type": "target_rate_shift",
      "product": "cash_loan",
      "dpd_bucket": "61-90",
      "segment": "new_high_risk",
      "model_name": "all",
      "model_version": "all",
      "optimizer_name": "all",
      "current_date": "2026-05-20",
      "previous_date": "2026-05-19",
      "current_period": "2026-05-20",
      "previous_period": "2026-05-19",
      "current_value": 0.39,
      "previous_value": 0.2307,
      "delta_abs": 0.1593,
      "delta_pp": 15.93,
      "delta_rel": 0.690507,
      "threshold_abs": 0.05,
      "severity": "critical",
      "cnt_clients": 4100,
      "event_type": "new_high_risk_segment",
      "is_expected_event": false,
      "is_expected_event_candidate": false,
      "python_description": "Метрика target_rate изменилась с 0.2307 до 0.39; зафиксирован алерт critical.",
      "business_zone": "target_behavior",
      "severity_weight": 3.0,
      "metric_weight": 0.85,
      "deviation_strength": 3.186,
      "volume_weight": 8.319,
      "priority_score": 67.5859
    },
    "related_alerts": [
      {
        "alert_id": "high_risk_share_growth_process_monitoring_cash_loan_2026-05-20_0020",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "high_risk_share",
        "alert_type": "high_risk_share_growth",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 0.49,
        "previous_value": 0.2221,
        "delta_abs": 0.2679,
        "delta_pp": 26.79,
        "delta_rel": 1.206213,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Доля high-risk клиентов изменилась с 0.2221 до 0.49; зафиксирован алерт critical.",
        "business_zone": "portfolio_risk",
        "severity_weight": 3.0,
        "metric_weight": 0.75,
        "deviation_strength": 2.679,
        "volume_weight": 8.319,
        "priority_score": 50.1448
      },
      {
        "alert_id": "volume_spike_process_monitoring_cash_loan_2026-05-20_0015",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "cnt_clients",
        "alert_type": "volume_spike",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 4100.0,
        "previous_value": 1795.0,
        "delta_abs": 2305.0,
        "delta_pp": 230500.0,
        "delta_rel": 1.284123,
        "threshold_abs": 0.7,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Количество клиентов изменилось с 1795 до 4100; зафиксирован алерт critical.",
        "business_zone": "volume",
        "severity_weight": 3.0,
        "metric_weight": 0.85,
        "deviation_strength": 1.8345,
        "volume_weight": 8.319,
        "priority_score": 38.916
      },
      {
        "alert_id": "avg_score_shift_process_monitoring_cash_loan_2026-05-20_0017",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "avg_score",
        "alert_type": "avg_score_shift",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 0.74,
        "previous_value": 0.5669,
        "delta_abs": 0.1731,
        "delta_pp": 17.31,
        "delta_rel": 0.305345,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Средний score изменился с 0.5669 до 0.74; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.8,
        "deviation_strength": 1.731,
        "volume_weight": 8.319,
        "priority_score": 34.5604
      },
      {
        "alert_id": "score_distribution_shift_process_monitoring_cash_loan_2026-05-20_0018",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "median_score",
        "alert_type": "score_distribution_shift",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 0.73,
        "previous_value": 0.5595,
        "delta_abs": 0.1705,
        "delta_pp": 17.05,
        "delta_rel": 0.304736,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Медианный score изменился с 0.5595 до 0.73; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.7,
        "deviation_strength": 1.705,
        "volume_weight": 8.319,
        "priority_score": 29.7861
      },
      {
        "alert_id": "score_distribution_shift_process_monitoring_cash_loan_2026-05-20_0019",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "p90_score",
        "alert_type": "score_distribution_shift",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 0.93,
        "previous_value": 0.7737,
        "delta_abs": 0.1563,
        "delta_pp": 15.63,
        "delta_rel": 0.202016,
        "threshold_abs": 0.1,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "90-й перцентиль score изменился с 0.7737 до 0.93; зафиксирован алерт critical.",
        "business_zone": "score_stability",
        "severity_weight": 3.0,
        "metric_weight": 0.7,
        "deviation_strength": 1.563,
        "volume_weight": 8.319,
        "priority_score": 27.3054
      },
      {
        "alert_id": "psi_score_growth_process_monitoring_cash_loan_2026-05-20_0021",
        "report_id": "demo_run",
        "process": "process_monitoring",
        "block": "Process monitoring",
        "metric": "psi_score",
        "alert_type": "psi_score_growth",
        "product": "cash_loan",
        "dpd_bucket": "61-90",
        "segment": "new_high_risk",
        "model_name": "all",
        "model_version": "all",
        "optimizer_name": "all",
        "current_date": "2026-05-20",
        "previous_date": "2026-05-19",
        "current_period": "2026-05-20",
        "previous_period": "2026-05-19",
        "current_value": 0.28,
        "previous_value": 0.0356,
        "delta_abs": 0.2444,
        "delta_pp": 24.44,
        "delta_rel": 6.865169,
        "threshold_abs": 0.2,
        "severity": "critical",
        "cnt_clients": 4100,
        "event_type": "new_high_risk_segment",
        "is_expected_event": false,
        "is_expected_event_candidate": false,
        "python_description": "Метрика psi_score изменилась с 0.0356 до 0.28; зафиксирован алерт critical.",
        "business_zone": "drift",
        "severity_weight": 3.0,
        "metric_weight": 0.8,
        "deviation_strength": 1.222,
        "volume_weight": 8.319,
        "priority_score": 24.3979
      }
    ],
    "group_priority_score": 272.6965,
    "alerts_count": 7,
    "critical_count": 7,
    "warning_count": 0,
    "info_count": 0,
    "metrics": [
      "avg_score",
      "cnt_clients",
      "high_risk_share",
      "median_score",
      "p90_score",
      "psi_score",
      "target_rate"
    ],
    "business_zones": [
      "drift",
      "portfolio_risk",
      "score_stability",
      "target_behavior",
      "volume"
    ],
    "is_expected_event": false
  },
  "alert_comment": {
    "alert_group_id": "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
    "short_title": "Рост доли high-risk клиентов и целевой ставки",
    "short_conclusion": "Наблюдается значительное увеличение доли high-risk клиентов и целевой ставки.",
    "facts": [
      "Зафиксировано критическое изменение целевой ставки с 0.2307 до 0.39.",
      "Увеличена доля high-risk клиентов с 0.2221 до 0.49.",
      "Общее количество клиентов увеличилось с 1795 до 4100.",
      "Средний и медианный scores выросли соответственно с 0.5669 и 0.5595 до 0.74 и 0.73.",
      "90-й перцентиль score увеличился с 0.7737 до 0.93.",
      "Показатель psi_score вырос с 0.0356 до 0.28."
    ],
    "business_interpretation": "Изменения указывают на возможное ухудшение качества кредитного портфеля.",
    "possible_causes": [
      "Сдвиг в составе клиентской базы или продуктов.",
      "Проблемы с качеством данных или моделью оценки рисков."
    ],
    "recommended_checks": [
      "Провести сегментный, продуктовый и DPD-анализ.",
      "Оценить изменения в объеме и составе новых сегментов.",
      "Сравнить текущую ситуацию с аналогичными периодами прошлого года."
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
  "alert_group_id": "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
  "selected_tools": [
    {
      "tool_name": "check_target_rate_shift",
      "reason": "Проверка изменения target_rate необходима для анализа аномального поведения целевой ставки.",
      "expected_evidence": "Изменение target_rate между текущим и предыдущим периодом."
    },
    {
      "tool_name": "check_score_distribution_shift",
      "reason": "Анализ распределения scores важен для выявления изменений в составе клиентской базы.",
      "expected_evidence": "Сдвиги в avg_score, median_score, p90_score и high_risk_share."
    },
    {
      "tool_name": "check_product_mix_shift",
      "reason": "Необходима проверка изменений в продуктовом составе для понимания влияния на risk profile.",
      "expected_evidence": "Доля продукта в процессе monitoring изменилась."
    },
    {
      "tool_name": "check_psi_shift",
      "reason": "PSI-метрика помогает оценить стабильность модели и выявить возможные сдвиги в распределении признаков.",
      "expected_evidence": "Изменения psi_score и psi_features."
    },
    {
      "tool_name": "check_volume_shift",
      "reason": "Необходимо понять влияние увеличения количества клиентов на общую картину.",
      "expected_evidence": "Относительное изменение cnt_clients и cnt_scored."
    }
  ],
  "stop_reason": ""
}
```
