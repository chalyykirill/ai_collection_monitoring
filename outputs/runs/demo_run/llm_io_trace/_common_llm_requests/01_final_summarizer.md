# Final Summarizer

## What this stage does

Формирует executive summary по всем alert groups, comments и investigation reports.

## Reconstruction note

`monitoring_data.csv` прочитан и содержит 390 строк. Текущий Final Summarizer builder не получает строки мониторинга напрямую; monitoring_stats восстановлен по той же логике, что и `run_final_summary.py`.

## Model input: rendered prompt

```text
# Роль
Ты Final Summarizer, автор executive summary мониторинга Collection.

# Цель
Сформировать компактное итоговое заключение для аналитика и руководителя.

# Контекст
Не пересказывай все алерты подряд. Разделяй expected events и potential incidents. Общий статус critical не отменяет и не скрывает ожидаемые события. Ожидаемые события не эскалируй как инциденты и не описывай их в manager_summary как проблему, сбой или ошибку. Используй investigation_reports как главный evidence layer.
Используй только переданные входные данные и документацию. Не придумывай факты, причины, результаты проверок или положения документации. Отделяй наблюдаемые факты от гипотез. Если данных недостаточно, используй needs_manual_review там, где это допускает схема. Проведи внутренний анализ, но не показывай ход рассуждений.

# Контекст документации
[process_monitoring/high_risk_segment.md] # Новый рискованный сегмент

Событие `new_high_risk_segment` не является заранее ожидаемым. Одновременный рост
`avg_score`, `median_score`, `p90_score`, `high_risk_share`, `target_rate` и
`psi_score` может указывать на изменение состава входящего потока.

До диагностики событие следует считать `pote

[common/metrics_dictionary.md] # Словарь метрик

- `cnt_clients` — количество клиентов в агрегированном срезе.
- `cnt_scored` — количество клиентов, для которых рассчитан score.
- `target_rate` — наблюдаемая доля целевого события.
- `gini` — качество ранжирования модели; заметное падение требует диагностики.
- `avg_score`, `media

[process_monitoring/anomaly_playbook.md] # Playbook мониторинга процесса

При скачке объема проверьте календарь известных событий, источник загрузки и
изменение продуктового состава.

При одновременном сдвиге риска и объема сравните текущий поток с предыдущим
периодом по `product`, `dpd_bucket` и `segment`. Не интерпретируйте рост score ка

[data_quality_monitoring/feature_vector_quality.md] # Качество feature vector

Событие `empty_feature_vector` означает рост доли пустых или частично
незаполненных входных признаков. Если alert group подтверждает превышение
порогов по `empty_feature_vector_share` или `feature_missing_rate`, само
отклонение классифицируется как `potential_incident` кач

[data_quality_monitoring/anomaly_playbook.md] # Playbook качества данных

При росте missing rate:

- локализовать пропуски по источникам и признакам;
- сравнить время обновления витрин;
- проверить объем пустых feature vector;
- оценить влияние пропусков на score;
- проверить восстановление после исправления загрузки.

Причину следует считать п

[optimizer_monitoring/optimizer_rules.md] # Правила бизнес-оптимизатора

Событие `optimizer_mass_reject` означает массовый рост решений reject или
no action одновременно с падением `cnt_approved_for_communication`. Это не
является штатным режимом и классифицируется как `potential_incident`.

Возможные причины: изменение правил, исчерпание б

[optimizer_monitoring/anomaly_playbook.md] # Playbook оптимизатора

При массовых отказах:

- проверить версии и условия бизнес-правил;
- проверить бюджетные и контактные ограничения;
- проверить входные признаки оптимизатора;
- проверить справочники доступных коммуникаций;
- сравнить reject share по каналам, продуктам и сегментам.

Массовое

[process_monitoring/credit_card_inflow.md] # Неритмичное поступление credit card

Событие `credit_card_batch_inflow` означает пакетное поступление портфеля
кредитных карт. Для подтвержденной даты загрузки это ожидаемая особенность
процесса, `expected_process_feature`.

Типичные признаки: рост `cnt_clients`, увеличение `product_share` и возмо

[common/known_events.md] # Известные события мониторинга

## bank_unavailable_day

Единый день недоступности банка (ЕДН) является плановым технологическим
событием, если дата подтверждена календарем работ и во входных данных установлен
признак `is_expected_event=true`.

В день ЕДН допустимы нулевые `cnt_clients`, `cnt_score

[model_monitoring/model_quality.md] # Качество модели

Событие `model_gini_drop` означает существенное снижение `gini`. Оно не является
ожидаемым и классифицируется как `potential_incident` до завершения диагностики.

Падение Gini может быть связано с изменением target rate, состава потока,
распределения score или качества признаков,

# Language policy
Все человекочитаемые текстовые поля верни строго на русском языке.
Не используй английские предложения.
Не используй транслитерацию.
Технические названия метрик, функций, JSON-полей и event_type можно оставлять как есть.
Примеры допустимых технических терминов: target_rate, psi_score, reject_share, check_psi_shift, model_gini_drop.
Ответ должен быть валидным JSON.

# Входные данные
{
  "monitoring_stats": {
    "alert_groups": 6,
    "critical_groups": 6,
    "warning_groups": 0,
    "expected_events": 2,
    "potential_incidents": 4,
    "needs_manual_review": 0
  },
  "alert_group_comments": [
    {
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
    },
    {
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
    },
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
    },
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
  ],
  "investigation_reports": [
    {
      "alert_group_id": "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
      "tool_findings": [
        {
          "tool_name": "check_target_rate_shift",
          "status": "critical",
          "finding": "target_rate изменился на 15.93 п.п.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_score_distribution_shift",
          "status": "critical",
          "finding": "Распределение score имеет общий статус critical.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_product_mix_shift",
          "status": "ok",
          "finding": "Доля продукта cash_loan изменилась на 4.02 п.п.",
          "supports_hypothesis": false
        },
        {
          "tool_name": "check_psi_shift",
          "status": "critical",
          "finding": "PSI-метрики имеют общий статус critical.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_volume_shift",
          "status": "critical",
          "finding": "Метрики объема имеют общий статус critical.",
          "supports_hypothesis": true
        }
      ],
      "investigation_report": {
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
    },
    {
      "alert_group_id": "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
      "tool_findings": [
        {
          "tool_name": "check_empty_feature_vector_growth",
          "status": "critical",
          "finding": "empty_feature_vector_share изменился на 10.73 п.п.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_missing_rate_growth",
          "status": "critical",
          "finding": "Метрики пропусков имеют общий статус critical.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_score_distribution_shift",
          "status": "critical",
          "finding": "Распределение score имеет общий статус critical.",
          "supports_hypothesis": true
        }
      ],
      "investigation_report": {
        "alert_group_id": "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
        "evidence_summary": [
          "Доля пустых feature vector увеличилась на 10.73 п.п.",
          "Доля пропущенных признаков увеличилась на 36.44 п.п.",
          "Средний score увеличился на 18.41 п.п.",
          "Медианный score увеличился на 18.64 п.п.",
          "90-й перцентиль score увеличился на 15.05 п.п.",
          "PSI признаков увеличился на 25.65 п.п."
        ],
        "root_cause_hypothesis": "Возможные причины включают проблемы с качеством исходных данных или технологические сбои в процессе их обработки.",
        "confidence": "high",
        "recommended_actions": [
          "Провести детальный анализ качества источников данных и процессов их загрузки.",
          "Оценить влияние увеличения доли пустых feature vector на ключевые показатели моделей."
        ],
        "needs_manual_review": false
      }
    },
    {
      "alert_group_id": "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
      "tool_findings": [
        {
          "tool_name": "check_optimizer_reject_share",
          "status": "critical",
          "finding": "Метрики отказов оптимизатора имеют статус critical.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_communication_mix_shift",
          "status": "critical",
          "finding": "Микс коммуникаций имеет общий статус critical.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_volume_shift",
          "status": "ok",
          "finding": "Метрики объема имеют общий статус ok.",
          "supports_hypothesis": false
        }
      ],
      "investigation_report": {
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
    },
    {
      "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
      "tool_findings": [
        {
          "tool_name": "check_product_mix_shift",
          "status": "critical",
          "finding": "Доля продукта credit_card изменилась на 26.19 п.п.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_target_rate_shift",
          "status": "warning",
          "finding": "target_rate изменился на 4.02 п.п.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_volume_shift",
          "status": "critical",
          "finding": "Метрики объема имеют общий статус critical.",
          "supports_hypothesis": true
        }
      ],
      "investigation_report": {
        "alert_group_id": "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
        "evidence_summary": [
          "Наблюдался резкий рост cnt_clients на 10399 единиц.",
          "Доля product_share увеличилась на 26.19 процентных пунктов.",
          "Событие credit_card_batch_inflow подтверждено как ожидаемое.",
          "Событие зарегистрировано в regular_flow сегменте."
        ],
        "root_cause_hypothesis": "Скачок объема и доли credit_card объясняется ожидаемым пакетным поступлением портфеля.",
        "confidence": "high",
        "recommended_actions": [
          "Контролировать завершение пакетной загрузки.",
          "Анализировать метрики с учетом продуктового микса."
        ],
        "needs_manual_review": false
      }
    },
    {
      "alert_group_id": "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop",
      "tool_findings": [
        {
          "tool_name": "check_target_rate_shift",
          "status": "critical",
          "finding": "target_rate изменился на 5.27 п.п.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_psi_shift",
          "status": "warning",
          "finding": "PSI-метрики имеют общий статус warning.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_score_distribution_shift",
          "status": "ok",
          "finding": "Распределение score имеет общий статус ok.",
          "supports_hypothesis": false
        }
      ],
      "investigation_report": {
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
    },
    {
      "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
      "tool_findings": [
        {
          "tool_name": "check_known_event_calendar",
          "status": "ok",
          "finding": "Известное событие bank_unavailable_day подтверждено признаком is_expected_event=true.",
          "supports_hypothesis": true
        },
        {
          "tool_name": "check_volume_shift",
          "status": "critical",
          "finding": "Метрики объема имеют общий статус critical.",
          "supports_hypothesis": true
        }
      ],
      "investigation_report": {
        "alert_group_id": "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day",
        "evidence_summary": [
          "Событие bank_unavailable_day подтверждено признаком is_expected_event=true.",
          "Объем клиентов упал до нуля.",
          "Метрики объема имеют общий статус critical."
        ],
        "root_cause_hypothesis": "Критичное отклонение объема объяснено подтвержденным ЕДН и не является инцидентом.",
        "confidence": "high",
        "recommended_actions": [
          "Контролировать восстановление потока после завершения ЕДН."
        ],
        "needs_manual_review": false
      }
    }
  ]
}

# Выходные данные
Приоритизируй наиболее важные инциденты и проверки. expected_events должен перечислить все группы из alert_group_comments с классификацией expected_event или expected_process_feature. В expected_events верни только точные alert_group_id этих групп, по одному идентификатору на элемент. potential_incidents должен перечислить все группы с классификацией potential_incident или needs_manual_review. В potential_incidents также верни только точные alert_group_id, по одному идентификатору на элемент. Не пропускай ни одной группы и не помещай одну группу в оба списка. root_cause_hypotheses бери только из investigation_reports групп с классификацией potential_incident или needs_manual_review; объяснения expected_event и expected_process_feature не включай в список первопричин инцидентов. Не добавляй гипотезу, которая отсутствует в investigation_reports. Объединяй дублирующиеся priority checks и сохраняй итог компактным.
Верни строго один JSON-объект без markdown-блоков, комментариев и текста вокруг JSON.

# Выходная JSON schema
{
  "additionalProperties": false,
  "properties": {
    "overall_status": {
      "enum": [
        "ok",
        "warning",
        "critical"
      ],
      "title": "Overall Status",
      "type": "string"
    },
    "executive_summary": {
      "title": "Executive Summary",
      "type": "string"
    },
    "expected_events": {
      "items": {
        "type": "string"
      },
      "title": "Expected Events",
      "type": "array"
    },
    "potential_incidents": {
      "items": {
        "type": "string"
      },
      "title": "Potential Incidents",
      "type": "array"
    },
    "root_cause_hypotheses": {
      "items": {
        "type": "string"
      },
      "title": "Root Cause Hypotheses",
      "type": "array"
    },
    "priority_checks": {
      "items": {
        "type": "string"
      },
      "title": "Priority Checks",
      "type": "array"
    },
    "manager_summary": {
      "title": "Manager Summary",
      "type": "string"
    }
  },
  "required": [
    "overall_status",
    "executive_summary",
    "expected_events",
    "potential_incidents",
    "root_cause_hypotheses",
    "priority_checks",
    "manager_summary"
  ],
  "title": "FinalSummary",
  "type": "object"
}
```

## Model output: saved JSON

```json
{
  "overall_status": "critical",
  "executive_summary": "Наблюдаются критические отклонения, связанные с ростом доли high-risk клиентов и целевой ставки, увеличением пустых feature vector, снижением качества ранжирования модели и массовыми отказами оптимизатора. Требуется детальная диагностика и корректирующие действия.",
  "expected_events": [
    "alert_group_002__process_monitoring__credit_card__1-30__regular_flow__all__all__credit_card_batch_inflow",
    "alert_group_001__process_monitoring__cash_loan__31-60__regular_flow__all__all__bank_unavailable_day"
  ],
  "potential_incidents": [
    "alert_group_005__process_monitoring__cash_loan__61-90__new_high_risk__all__all__new_high_risk_segment",
    "alert_group_004__data_quality_monitoring__cash_loan__31-60__base__collection_score_v1__all__empty_feature_vector",
    "alert_group_006__optimizer_monitoring__cash_loan__31-60__regular_flow__all__collection_contact_optimizer__optimizer_mass_reject",
    "alert_group_003__model_monitoring__credit_card__31-60__base__collection_score_v1__all__model_gini_drop"
  ],
  "root_cause_hypotheses": [
    "причина инцидента связана с изменением состава клиентской базы или проблемами качества данных и моделей оценки рисков",
    "возможные причины включают проблемы с качеством исходных данных или технологические сбои в процессе их обработки",
    "возможные причины инцидента включают изменения в правилах или условиях работы оптимизатора, проблемы с доступными коммуникациями или их настройками, а также недостаточный бюджет или исчерпание лимитов оптимизатора",
    "возможные причины снижения качества ранжирования модели включают изменение целевой ставки или состава клиентской базы, изменения в распределении скоринга и ухудшение качества признаков"
  ],
  "priority_checks": [
    "детальный анализ изменений в составе клиентской базы и продуктах",
    "оценка изменений в качестве данных и моделей оценки рисков",
    "проведение детального анализа качества источников данных и процессов их загрузки",
    "оценка влияния увеличения доли пустых feature vector на ключевые показатели моделей",
    "детальный аудит изменений в правилах и условиях оптимизатора",
    "проверка доступных и настроенных каналов коммуникаций",
    "оценка текущего бюджета и лимитов оптимизатора",
    "углубленный анализ изменений в составе клиентской базы",
    "оценка распределения скоринга и его стабильности",
    "проверка качества и полноты используемых признаков"
  ],
  "manager_summary": "Необходимо срочно провести диагностику причин критических отклонений и принять меры для стабилизации ситуации. Особое внимание уделить изменениям в составе клиентской базы, качеству данных и моделей оценки рисков, а также работе оптимизатора и качеству моделей."
}
```
