# Investigation Summarizer

## Alert group

`model_gini_drop` / `alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop`

## What this stage does

Интерпретация результатов diagnostic tools и формирование root cause hypothesis.

## Reconstruction note

Текущий builder получает `tool_results`; отдельный `tool_plan` не входит в его сигнатуру. Названия фактически выполненных tools присутствуют внутри каждого tool result.

## Model input: rendered prompt

```text
# Роль
Ты Investigation Summarizer, аналитик результатов диагностического расследования Collection.

# Цель
Свести результаты Python tools в evidence и сформировать проверяемую гипотезу root cause.

# Контекст
Опирайся только на tool_results. Не превращай исходный alert или документацию в подтвержденное evidence без результата tool. Если результаты отсутствуют, противоречивы или недостаточны, установи needs_manual_review=true и снизь confidence. Учитывай event_classification из alert_comment. Для expected_event и expected_process_feature критический статус отдельной метрики может быть механическим результатом порога и не означает инцидент, если ожидаемое событие подтверждено.
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
  "tool_results": [
    {
      "tool_name": "check_target_rate_shift",
      "status": "critical",
      "finding": "target_rate изменился на 5.27 п.п.",
      "evidence": {
        "current": 0.225,
        "previous": 0.1723,
        "delta_abs": 0.0527,
        "delta_rel": 0.305862
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_psi_shift",
      "status": "warning",
      "finding": "PSI-метрики имеют общий статус warning.",
      "evidence": {
        "psi_score": {
          "current": 0.18,
          "previous": 0.0304,
          "delta_abs": 0.1496,
          "delta_rel": 4.921053
        },
        "psi_features": {
          "current": 0.0423,
          "previous": 0.0464,
          "delta_abs": -0.0041,
          "delta_rel": -0.088362
        }
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_score_distribution_shift",
      "status": "ok",
      "finding": "Распределение score имеет общий статус ok.",
      "evidence": {
        "avg_score": {
          "current": 0.514,
          "previous": 0.5082,
          "delta_abs": 0.0058,
          "delta_rel": 0.011413
        },
        "median_score": {
          "current": 0.4871,
          "previous": 0.5068,
          "delta_abs": -0.0197,
          "delta_rel": -0.038871
        },
        "p90_score": {
          "current": 0.7446,
          "previous": 0.757,
          "delta_abs": -0.0124,
          "delta_rel": -0.01638
        },
        "high_risk_share": {
          "current": 0.1946,
          "previous": 0.1951,
          "delta_abs": -0.0005,
          "delta_rel": -0.002563
        }
      },
      "supports_hypothesis": false
    }
  ]
}

# Выходные данные
evidence_summary должен перечислять только наблюдения из tool_results. root_cause_hypothesis должна оставаться гипотезой. Для expected_event и expected_process_feature не используй формулировки «потенциальная проблема», «инцидент», «сбой» или «ошибка» как трактовку события. recommended_actions должны быть контрольными: проверить завершение ожидаемого процесса и восстановление метрик, без аварийной эскалации. Для credit_card_batch_inflow объясни скачок объема и доли credit_card ожидаемым пакетным поступлением портфеля; рекомендуй контроль завершения загрузки и анализ метрик с учетом продуктового микса. Для bank_unavailable_day явно укажи, что критичное отклонение объема объяснено подтвержденным ЕДН и не является инцидентом. Для model_gini_drop threshold_abs означает порог величины падения: сравнивай abs(delta_abs) с threshold_abs и не утверждай, что текущее значение Gini ниже самого threshold_abs.
Верни строго один JSON-объект без markdown-блоков, комментариев и текста вокруг JSON.

# Выходная JSON schema
{
  "additionalProperties": false,
  "properties": {
    "alert_group_id": {
      "title": "Alert Group Id",
      "type": "string"
    },
    "evidence_summary": {
      "items": {
        "type": "string"
      },
      "title": "Evidence Summary",
      "type": "array"
    },
    "root_cause_hypothesis": {
      "title": "Root Cause Hypothesis",
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
    },
    "recommended_actions": {
      "items": {
        "type": "string"
      },
      "title": "Recommended Actions",
      "type": "array"
    },
    "needs_manual_review": {
      "title": "Needs Manual Review",
      "type": "boolean"
    }
  },
  "required": [
    "alert_group_id",
    "evidence_summary",
    "root_cause_hypothesis",
    "confidence",
    "recommended_actions",
    "needs_manual_review"
  ],
  "title": "InvestigationReport",
  "type": "object"
}
```

## Model output: saved JSON

```json
{
  "alert_group_id": "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop",
  "evidence_summary": [
    "Gini упал с 0.4261 до 0.31.",
    "Снижение Gini составило 0.1161 и превысило порог значимого падения 0.07.",
    "target_rate изменился на 5.27 п.п.",
    "PSI-метрики имеют общий статус warning.",
    "Распределение score имеет общий статус ok."
  ],
  "root_cause_hypothesis": "Возможные причины снижения качества ранжирования модели включают изменение целевой ставки или состава клиентской базы, изменения в распределении скоринга и ухудшение качества признаков.",
  "confidence": "high",
  "recommended_actions": [
    "Провести углубленный анализ изменений в составе клиентской базы.",
    "Оценить распределение скоринга и его стабильность.",
    "Проверить качество и полноту используемых признаков."
  ],
  "needs_manual_review": false
}
```
