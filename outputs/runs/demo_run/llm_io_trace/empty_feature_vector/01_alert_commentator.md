# Alert Commentator

## Alert group

`empty_feature_vector` / `alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector`

## What this stage does

Первичная интерпретация alert group с учетом RAG-контекста.

## Reconstruction note

Полный RAG-контекст восстановлен повторным offline retrieval через `src.rag.retrieve_context`. Query, source, score и первые 300 символов каждого chunk совпали с `retrieved_contexts.json`. Исходный полный context_text отдельно в demo artifacts не сохранялся.

## Model input: rendered prompt

```text
# Роль
Ты Alert Commentator, аналитик первичной интерпретации мониторинга Collection.

# Цель
Сформировать краткий бизнесовый комментарий по одной alert group и классифицировать событие.

# Контекст
bank_unavailable_day классифицируй как expected_event только при подтверждении документацией. credit_card_batch_inflow классифицируй как expected_process_feature только при таком подтверждении. model_gini_drop, empty_feature_vector, new_high_risk_segment и optimizer_mass_reject обычно требуют potential_incident или needs_manual_review.
Используй только переданные входные данные и документацию. Не придумывай факты, причины, результаты проверок или положения документации. Отделяй наблюдаемые факты от гипотез. Если данных недостаточно, используй needs_manual_review там, где это допускает схема. Проведи внутренний анализ, но не показывай ход рассуждений.

# Контекст документации
[Источник: data_quality_monitoring/feature_vector_quality.md; relevance=0.0627]
# Качество feature vector

Событие `empty_feature_vector` означает рост доли пустых или частично
незаполненных входных признаков. Если alert group подтверждает превышение
порогов по `empty_feature_vector_share` или `feature_missing_rate`, само
отклонение классифицируется как `potential_incident` качества данных.
`needs_manual_review` следует использовать только если факт роста не
подтвержден входными метриками или данные противоречат друг другу.

Рост `empty_feature_vector_share` и `feature_missing_rate` может приводить к
резкому изменению `avg_score`, `median_score`, `p90_score` и `psi_features`.
Сдвиг score в этом случае нельзя автоматически считать реальным ростом риска.
Конкретная техническая root cause остается гипотезой до диагностики, но это не
отменяет классификацию наблюдаемого отклонения как потенциального инцидента.

Проверки: источники признаков, витрина подготовки данных, даты обновления,
заполненность ключевых полей и доля fallback-значений модели.

[Источник: common/metrics_dictionary.md; relevance=0.0589]
# Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `median_score`, `p90_score` — характеристики распределения score.
- `high_risk_share` — доля клиентов в зоне высокого риска.
- `psi_score` — сдвиг распределения score относительно базового периода.
- `psi_features` — сдвиг распределений признаков.
- `feature_missing_rate` — доля пропущенных значений признаков.
- `empty_feature_vector_share` — доля полностью пустых feature vector.
- `reject_share` — доля отказов или решений no action оптимизатора.
- `cnt_approved_for_communication` — число разрешенных коммуникаций.
- `unknown_communication_share` — доля решений с неизвестным типом коммуникации.

[Источник: data_quality_monitoring/anomaly_playbook.md; relevance=0.0119]
# Playbook качества данных

При росте missing rate:

- локализовать пропуски по источникам и признакам;
- сравнить время обновления витрин;
- проверить объем пустых feature vector;
- оценить влияние пропусков на score;
- проверить восстановление после исправления загрузки.

Причину следует считать подтвержденной только после проверки данных.

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
  }
}

# Выходные данные
Факты должны следовать из alert group или документации. possible_causes являются только проверяемыми гипотезами. Если event_classification равен expected_event или expected_process_feature, не называй событие инцидентом в short_title, short_conclusion и business_interpretation. Используй формулировки «ожидаемое событие» или «ожидаемая особенность процесса». Для model_gini_drop поле threshold_abs является порогом величины падения Gini, а не минимально допустимым значением Gini. Сравнивай abs(delta_abs) с threshold_abs. Например, при current_value=0.31, previous_value=0.4261 и threshold_abs=0.07 пиши: «Снижение Gini составило 0.1161 и превысило порог значимого падения 0.07». Никогда не пиши, что значение Gini 0.31 ниже порога 0.07.
Верни строго один JSON-объект без markdown-блоков, комментариев и текста вокруг JSON.

# Выходная JSON schema
{
  "additionalProperties": false,
  "properties": {
    "alert_group_id": {
      "title": "Alert Group Id",
      "type": "string"
    },
    "short_title": {
      "title": "Short Title",
      "type": "string"
    },
    "short_conclusion": {
      "title": "Short Conclusion",
      "type": "string"
    },
    "facts": {
      "items": {
        "type": "string"
      },
      "title": "Facts",
      "type": "array"
    },
    "business_interpretation": {
      "title": "Business Interpretation",
      "type": "string"
    },
    "possible_causes": {
      "items": {
        "type": "string"
      },
      "title": "Possible Causes",
      "type": "array"
    },
    "recommended_checks": {
      "items": {
        "type": "string"
      },
      "title": "Recommended Checks",
      "type": "array"
    },
    "event_classification": {
      "enum": [
        "expected_event",
        "expected_process_feature",
        "potential_incident",
        "needs_manual_review"
      ],
      "title": "Event Classification",
      "type": "string"
    },
    "risk_level": {
      "enum": [
        "low",
        "medium",
        "high"
      ],
      "title": "Risk Level",
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
    }
  },
  "required": [
    "alert_group_id",
    "short_title",
    "short_conclusion",
    "facts",
    "business_interpretation",
    "possible_causes",
    "recommended_checks",
    "event_classification",
    "risk_level",
    "confidence"
  ],
  "title": "AlertGroupComment",
  "type": "object"
}

# Примеры
[
  {
    "input": {
      "alert_group": {
        "alert_group_id": "example_edn",
        "event_type": "bank_unavailable_day",
        "is_expected_event": true,
        "metrics": [
          "cnt_clients",
          "null_metrics_rate"
        ]
      },
      "doc_context": "Дата входит в календарь ЕДН. В этот день допустимы нулевые объемы и NULL в мониторинге."
    },
    "output": {
      "alert_group_id": "example_edn",
      "short_title": "ЕДН подтвержден календарем",
      "short_conclusion": "Отклонение соответствует ожидаемому событию.",
      "facts": [
        "Объем снизился до нуля.",
        "Документация подтверждает ЕДН на эту дату."
      ],
      "business_interpretation": "Наблюдаемое отклонение объясняется технологическим событием.",
      "possible_causes": [
        "Плановый единый день недоступности банка."
      ],
      "recommended_checks": [
        "Проверить восстановление потока после завершения ЕДН."
      ],
      "event_classification": "expected_event",
      "risk_level": "low",
      "confidence": "high"
    }
  },
  {
    "input": {
      "alert_group": {
        "alert_group_id": "example_optimizer",
        "event_type": "optimizer_mass_reject",
        "is_expected_event": false,
        "metrics": [
          "reject_share",
          "cnt_approved_for_communication"
        ]
      },
      "doc_context": "Массовый рост отказов не является штатным режимом и требует проверки правил, бюджетов и справочников."
    },
    "output": {
      "alert_group_id": "example_optimizer",
      "short_title": "Массовые отказы оптимизатора",
      "short_conclusion": "Наблюдается потенциально критичное отклонение бизнес-логики.",
      "facts": [
        "Доля отказов выросла.",
        "Количество одобренных коммуникаций снизилось."
      ],
      "business_interpretation": "Оптимизатор ограничивает коммуникации значительно сильнее обычного.",
      "possible_causes": [
        "Изменение правил или бюджетных ограничений.",
        "Некорректный справочник коммуникаций."
      ],
      "recommended_checks": [
        "Проверить правила и ограничения оптимизатора.",
        "Проверить входные данные и справочники."
      ],
      "event_classification": "potential_incident",
      "risk_level": "high",
      "confidence": "high"
    }
  }
]
```

## Model output: saved JSON

```json
{
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
}
```
