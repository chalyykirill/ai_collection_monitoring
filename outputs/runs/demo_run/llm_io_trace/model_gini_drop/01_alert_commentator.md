# Alert Commentator

## Alert group

`model_gini_drop` / `alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop`

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
[Источник: model_monitoring/model_quality.md; relevance=0.0907]
# Качество модели

Событие `model_gini_drop` означает существенное снижение `gini`. Оно не является
ожидаемым и классифицируется как `potential_incident` до завершения диагностики.

Падение Gini может быть связано с изменением target rate, состава потока,
распределения score или качества признаков, но эти причины являются гипотезами.

Основные метрики: `gini`, `target_rate`, `psi_score`, `psi_features`,
`avg_score`, `high_risk_share`.

[Источник: common/metrics_dictionary.md; relevance=0.0158]
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

[Источник: common/known_events.md; relevance=0.0065]
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
}
```
