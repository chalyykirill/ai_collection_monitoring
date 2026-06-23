# Investigation Summarizer

## Alert group

`new_high_risk_segment` / `alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment`

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
  "tool_results": [
    {
      "tool_name": "check_target_rate_shift",
      "status": "critical",
      "finding": "target_rate изменился на 15.93 п.п.",
      "evidence": {
        "current": 0.39,
        "previous": 0.2307,
        "delta_abs": 0.1593,
        "delta_rel": 0.690507
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_score_distribution_shift",
      "status": "critical",
      "finding": "Распределение score имеет общий статус critical.",
      "evidence": {
        "avg_score": {
          "current": 0.74,
          "previous": 0.5669,
          "delta_abs": 0.1731,
          "delta_rel": 0.305345
        },
        "median_score": {
          "current": 0.73,
          "previous": 0.5595,
          "delta_abs": 0.1705,
          "delta_rel": 0.304736
        },
        "p90_score": {
          "current": 0.93,
          "previous": 0.7737,
          "delta_abs": 0.1563,
          "delta_rel": 0.202016
        },
        "high_risk_share": {
          "current": 0.49,
          "previous": 0.2221,
          "delta_abs": 0.2679,
          "delta_rel": 1.206213
        }
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_product_mix_shift",
      "status": "ok",
      "finding": "Доля продукта cash_loan изменилась на 4.02 п.п.",
      "evidence": {
        "product": "cash_loan",
        "current_share": 0.767218,
        "previous_share": 0.727044,
        "delta_pp": 4.0174,
        "current_product_clients": 16598,
        "previous_product_clients": 13587,
        "current_total_clients": 21634,
        "previous_total_clients": 18688
      },
      "supports_hypothesis": false
    },
    {
      "tool_name": "check_psi_shift",
      "status": "critical",
      "finding": "PSI-метрики имеют общий статус critical.",
      "evidence": {
        "psi_score": {
          "current": 0.28,
          "previous": 0.0356,
          "delta_abs": 0.2444,
          "delta_rel": 6.865169
        },
        "psi_features": {
          "current": 0.0353,
          "previous": 0.0503,
          "delta_abs": -0.015,
          "delta_rel": -0.298211
        }
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_volume_shift",
      "status": "critical",
      "finding": "Метрики объема имеют общий статус critical.",
      "evidence": {
        "cnt_clients": {
          "current": 4100.0,
          "previous": 1795.0,
          "delta_abs": 2305.0,
          "delta_rel": 1.284123
        },
        "cnt_scored": {
          "current": 3950.0,
          "previous": 1700.0,
          "delta_abs": 2250.0,
          "delta_rel": 1.323529
        }
      },
      "supports_hypothesis": true
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
  "alert_group_id": "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
  "evidence_summary": [
    "целевая ставка изменилась с 0.2307 до 0.39",
    "доля high-risk клиентов увеличилась с 0.2221 до 0.49",
    "общее количество клиентов выросло с 1795 до 4100",
    "средний score повысился с 0.5669 до 0.74",
    "медианный score вырос с 0.5595 до 0.73",
    "90-й перцентиль score увеличился с 0.7737 до 0.93",
    "psi_score вырос с 0.0356 до 0.28"
  ],
  "root_cause_hypothesis": "причина инцидента связана с изменением состава клиентской базы или проблемами качества данных и моделей оценки рисков",
  "confidence": "high",
  "recommended_actions": [
    "провести детальный анализ изменений в составе клиентской базы и продуктах",
    "оценить изменения в качестве данных и моделях оценки рисков",
    "сравнить текущую ситуацию с аналогичными периодами прошлых лет"
  ],
  "needs_manual_review": false
}
```
