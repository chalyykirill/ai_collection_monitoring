# Alert Commentator

## Alert group

`credit_card_batch_inflow` / `alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow`

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
[Источник: process_monitoring/credit_card_inflow.md; relevance=0.0648]
# Неритмичное поступление credit card

Событие `credit_card_batch_inflow` означает пакетное поступление портфеля
кредитных карт. Для подтвержденной даты загрузки это ожидаемая особенность
процесса, `expected_process_feature`.

Типичные признаки: рост `cnt_clients`, увеличение `product_share` и возможный
сдвиг `target_rate`.

Проверки:

- календарь и статус пакетной загрузки;
- полнота поступившего портфеля;
- доля `credit_card` в общем потоке;
- target rate внутри продукта и без эффекта продуктового микса.

[Источник: common/known_events.md; relevance=0.0470]
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

[Источник: common/metrics_dictionary.md; relevance=0.0447]
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
}
```
