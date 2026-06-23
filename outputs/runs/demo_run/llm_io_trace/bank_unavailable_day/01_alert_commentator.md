# Alert Commentator

## Alert group

`bank_unavailable_day` / `alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day`

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
[Источник: common/metrics_dictionary.md; relevance=0.0416]
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

[Источник: common/known_events.md; relevance=0.0380]
# Известные события мониторинга

## bank_unavailable_day

Единый день недоступности банка (ЕДН) является плановым технологическим
событием, если дата подтверждена календарем работ и во входных данных установлен
признак `is_expected_event=true`.

В день ЕДН допустимы нулевые `cnt_clients`, `cnt_scored` и пропуски в зависимых
метриках. Такое отклонение классифицируется как `expected_event`, а не как
деградация процесса.

Рекомендуемые проверки:

- сверить дату с календарем ЕДН;
- проверить восстановление потока на следующем доступном дне;
- исключить день ЕДН из обычного сравнения динамики.

## credit_card_batch_inflow

Портфель `credit_card` может поступать неритмичными пакетами. Если дата
подтверждена календарем загрузок и установлен `is_expected_event=true`, скачок
объема и доли продукта является `expected_process_feature`.

Следует проверить завершение загрузки, `cnt_clients`, `product_share`,
`target_rate` и метрики процесса без влияния продуктового микса.

[Источник: process_monitoring/high_risk_segment.md; relevance=0.0077]
# Новый рискованный сегмент

Событие `new_high_risk_segment` не является заранее ожидаемым. Одновременный рост
`avg_score`, `median_score`, `p90_score`, `high_risk_share`, `target_rate` и
`psi_score` может указывать на изменение состава входящего потока.

До диагностики событие следует считать `potential_incident`, а изменение состава
портфеля — гипотезой.

Проверки:

- сегментный, продуктовый и DPD-микс;
- объем нового сегмента;
- распределение score по сегментам;
- target rate и PSI внутри сопоставимых срезов.

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
}
```
