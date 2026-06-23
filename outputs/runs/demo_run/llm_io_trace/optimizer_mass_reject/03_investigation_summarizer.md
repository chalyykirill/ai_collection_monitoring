# Investigation Summarizer

## Alert group

`optimizer_mass_reject` / `alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject`

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
  "tool_results": [
    {
      "tool_name": "check_optimizer_reject_share",
      "status": "critical",
      "finding": "Метрики отказов оптимизатора имеют статус critical.",
      "evidence": {
        "reject_share": {
          "current": 0.83,
          "previous": 0.1949,
          "delta_abs": 0.6351,
          "delta_rel": 3.258594
        },
        "cnt_approved_for_communication": {
          "current": 1350.0,
          "previous": 7401.0,
          "delta_abs": -6051.0,
          "delta_rel": -0.817592
        },
        "cnt_rejected_by_optimizer": {
          "current": 9100.0,
          "previous": 2116.0,
          "delta_abs": 6984.0,
          "delta_rel": 3.300567
        }
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_communication_mix_shift",
      "status": "critical",
      "finding": "Микс коммуникаций имеет общий статус critical.",
      "evidence": {
        "communication_call_share": {
          "current": 0.03,
          "previous": 0.3033,
          "delta_abs": -0.2733,
          "delta_rel": -0.901088
        },
        "communication_visit_share": {
          "current": 0.02,
          "previous": 0.1551,
          "delta_abs": -0.1351,
          "delta_rel": -0.871051
        },
        "communication_sms_share": {
          "current": 0.04,
          "previous": 0.2494,
          "delta_abs": -0.2094,
          "delta_rel": -0.839615
        },
        "communication_waiting_share": {
          "current": 0.02,
          "previous": 0.1394,
          "delta_abs": -0.1194,
          "delta_rel": -0.856528
        },
        "communication_agency_share": {
          "current": 0.01,
          "previous": 0.0889,
          "delta_abs": -0.0789,
          "delta_rel": -0.887514
        },
        "unknown_communication_share": {
          "current": 0.18,
          "previous": 0.0096,
          "delta_abs": 0.1704,
          "delta_rel": 17.75
        }
      },
      "supports_hypothesis": true
    },
    {
      "tool_name": "check_volume_shift",
      "status": "ok",
      "finding": "Метрики объема имеют общий статус ok.",
      "evidence": {
        "cnt_clients": {
          "current": 10831.0,
          "previous": 10856.0,
          "delta_abs": -25.0,
          "delta_rel": -0.002303
        },
        "cnt_scored": {
          "current": null,
          "previous": null,
          "delta_abs": null,
          "delta_rel": null
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
  "alert_group_id": "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
  "evidence_summary": [
    "Доля отказов оптимизатора значительно увеличилась с 0.1949 до 0.83.",
    "Количество одобренных коммуникаций резко сократилось с 7401 до 1350.",
    "Доля неизвестных коммуникаций возросла с 0.0096 до 0.18.",
    "Микс коммуникаций показал критическое снижение всех типов коммуникаций.",
    "Метрики отказов оптимизатора имеют статус critical.",
    "Микс коммуникаций имеет общий статус critical."
  ],
  "root_cause_hypothesis": "Возможные причины инцидента включают изменения в правилах или условиях работы оптимизатора, проблемы с доступными коммуникациями или их настройками, а также недостаточный бюджет или исчерпание лимитов оптимизатора.",
  "confidence": "high",
  "recommended_actions": [
    "Детально проанализировать изменения в правилах и условиях оптимизатора.",
    "Провести проверку доступных и настроенных каналов коммуникаций.",
    "Оценить текущий бюджет и лимиты оптимизатора."
  ],
  "needs_manual_review": false
}
```
