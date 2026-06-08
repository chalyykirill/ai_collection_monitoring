# Collection Monitoring Agent

AI-агент для анализа регулярного мониторинга процессов, моделей, оптимизаторов и качества данных в Collection.

Проект создается для хакатона **"Агенты в Collection"**. MVP демонстрирует, как AI может помогать аналитику быстрее разбирать большие мониторинговые отчеты: автоматически находить отклонения, отличать ожидаемые технологические/процессные события от потенциальных инцидентов и формировать бизнесовое резюме по результатам мониторинга.

---

## 1. Основная идея

В регулярном мониторинге Collection может быть много графиков, таблиц и проверок. Аналитик вручную просматривает отчет, ищет скачки, просадки, NULL-значения, сдвиги распределений, проблемы качества модели и неожиданные решения оптимизатора.

**Collection Monitoring Agent** автоматизирует этот процесс:

1. Python считает агрегаты мониторинга.
2. Python запускает проверки и формирует `alert objects`.
3. Python группирует связанные алерты в `alert groups`.
4. Для top-priority alert groups подбирается RAG-контекст по документации процесса.
5. LLM формирует структурированный комментарий по группе алертов.
6. LLM формирует финальное summary по мониторингу в целом.
7. Система генерирует human report и архив запуска.

Главный принцип:

> **Python считает факты. LLM объясняет факты бизнесовым языком с учетом документации.**

---

## 2. Главная ценность демо

Не каждое статистическое отклонение является проблемой.

Например:

- NULL/0 в день ЕДН может быть ожидаемым технологическим событием;
- всплеск потока кредитных карт может быть нормальной особенностью процесса загрузки;
- падение Gini модели может быть признаком деградации качества модели;
- скачок среднего score может быть связан не с ростом риска, а с пустым вектором признаков;
- массовый отказ оптимизатора по всем коммуникациям может быть критичным сбоем бизнес-логики.

MVP показывает, что агент не просто фиксирует отклонение, а использует документацию процесса и формирует корректную бизнес-интерпретацию:

1. Отклонение ожидаемо и объясняется документацией.
2. Отклонение похоже на техническую проблему.
3. Отклонение похоже на модельную/процессную деградацию и требует проверки.

---

## 3. Что проект делает

MVP должен уметь:

- генерировать синтетические агрегированные данные мониторинга Collection;
- считать метрики по периодам и срезам;
- сравнивать текущий период с предыдущим;
- находить отклонения по заданным правилам;
- формировать `alert objects`;
- группировать связанные алерты в `alert groups`;
- ранжировать alert groups по `priority_score`;
- подбирать документацию по процессу и типу алерта;
- получать комментарий LLM по top alert groups;
- получать финальное summary по мониторингу;
- формировать отчет для человека;
- сохранять архив запуска для аудита и будущего развития.

---

## 4. Что проект НЕ делает

В MVP не нужно делать:

- работу с реальными клиентскими данными;
- принятие решений по конкретным клиентам;
- оптимизацию коммуникаций вместо существующих моделей;
- production-ready интеграцию с Confluence;
- полноценный historical RAG по прошлым мониторингам;
- сложный multi-agent workflow;
- передачу 200 графиков напрямую в LLM;
- сложную авторизацию, роли и права доступа;
- полноценную web-платформу.

Проект работает на **синтетических агрегированных данных**.

---

## 5. Главные демо-сценарии

Данные должны отражать несколько реалистичных кейсов мониторинга процессов и моделей Collection.

### Демо-кейс 1. Единый день недоступности банка, ЕДН

В один из дней мониторинга значения ряда метрик становятся `NULL` или `0`, потому что в банке проходит ЕДН — единый день недоступности, связанный с обновлением инфраструктуры.

Ожидаемое поведение агента:

- Python фиксирует алерт: резкое падение объема, `NULL`/`0` в метриках;
- RAG подтягивает документацию про ЕДН, сверяет с потенциальным календарем  ЕДН;
- LLM объясняет, что это ожидаемое технологическое событие, а не деградация процесса;
- рекомендация: проверить, что дата совпадает с календарем ЕДН, и не учитывать этот день в регулярной оценке динамики.

### Демо-кейс 2. Неритмичное поступление портфеля кредитных карт

Портфель по продукту `credit_card` поступает в общий поток неравномерно. В отдельные дни возникают всплески объема, из-за чего срабатывают алерты по количеству клиентов, доле продукта или target rate.

Ожидаемое поведение агента:

- Python фиксирует всплеск объема/доли продукта;
- RAG подтягивает описание особенности загрузки портфеля кредитных карт;
- LLM объясняет, что всплеск может быть нормальной особенностью процесса, если он совпадает с ожидаемыми днями поступления потока;
- рекомендация: сверить дату с календарем загрузки и отдельно смотреть метрики без учета продуктового микса.

### Демо-кейс 3. Падение Gini модели

В мониторинге качества модели падает Gini. Это может указывать на деградацию модели, изменение состава потока, изменение target rate или проблему с признаками.

Ожидаемое поведение агента:

- Python фиксирует падение Gini относительно предыдущего периода или порога;
- RAG подтягивает документацию по мониторингу качества моделей;
- LLM формирует вывод: падение Gini требует проверки target rate, PSI, распределения score, пустых признаков и изменения состава портфеля.

### Демо-кейс 4. Пустой вектор признаков на входе модели

В один из периодов в модель попадает пустой или частично пустой feature vector. Из-за этого резко меняется средний score или распределение score.

Ожидаемое поведение агента:

- Python фиксирует рост missing rate, скачок среднего score и/или изменение распределения score;
- RAG подтягивает документацию по входному вектору модели;
- LLM объясняет, что резкое изменение score может быть связано не с изменением риска клиентов, а с проблемой качества данных;
- рекомендация: проверить заполненность признаков, пайплайн подготовки витрины и дату обновления источников.

### Демо-кейс 5. Новый рискованный сегмент в потоке

В поток попадает новый сегмент клиентов с более высоким риском. Среднее значение score растет, распределение score смещается вправо, может измениться target rate.

Ожидаемое поведение агента:

- Python фиксирует сдвиг распределения score, рост среднего score и изменение доли high-risk клиентов;
- RAG подтягивает описание сегментов и интерпретации score;
- LLM объясняет, что изменение может быть связано с изменением состава входящего потока, а не обязательно с ошибкой модели;
- рекомендация: проверить продуктовый/DPD/сегментный микс и сравнить распределение score по сегментам.

### Демо-кейс 6. Бизнес-оптимизатор начал делать отказы по всем коммуникациям

В мониторинге оптимизатора резко растет доля решения `reject` или `no_action` по всем коммуникациям. Это может быть связано с изменением правил, некорректным ограничением бюджета или технической ошибкой в бизнес-логике.

Ожидаемое поведение агента:

- Python фиксирует аномальный рост доли отказов по коммуникациям;
- RAG подтягивает документацию по логике бизнес-оптимизатора;
- LLM объясняет, что массовый отказ по всем коммуникациям является потенциально критичным отклонением;
- рекомендация: проверить правила оптимизатора, бюджетные ограничения, входные признаки и корректность справочников коммуникаций.

---

## 6. Архитектура

Общая схема:

```text
Synthetic monitoring data
        ↓
Python monitoring engine
        ↓
Anomaly detector
        ↓
Alert objects
        ↓
Alert grouping + priority scoring
        ↓
RAG documentation context
        ↓
LLM comments by alert group
        ↓
Final LLM summary
        ↓
Human report + run archive
```

---

## 7. Структура проекта

Предпочтительная структура:

```text
collection_monitoring_agent/
│
├── README.md
├── requirements.txt
├── run_pipeline.py
│
├── data/
│   └── monitoring_data.csv
│
├── docs/
│   ├── common/
│   │   ├── metrics_dictionary.md
│   │   ├── monitoring_rules.md
│   │   └── known_events.md
│   │
│   ├── process_monitoring/
│   │   ├── process_description.md
│   │   └── anomaly_playbook.md
│   │
│   ├── model_monitoring/
│   │   ├── process_description.md
│   │   └── anomaly_playbook.md
│   │
│   ├── optimizer_monitoring/
│   │   ├── process_description.md
│   │   └── anomaly_playbook.md
│   │
│   └── data_quality_monitoring/
│       ├── process_description.md
│       └── anomaly_playbook.md
│
├── outputs/
│   └── runs/
│       └── demo_run/
│           ├── monitoring_data.csv
│           ├── alert_objects.json
│           ├── alert_groups.json
│           ├── alert_group_comments.json
│           ├── final_summary.json
│           ├── history_summary.json
│           └── human_report.md
│
└── src/
    ├── generate_demo_data.py
    ├── detect_anomalies.py
    ├── group_alerts.py
    ├── rag.py
    ├── prompts.py
    ├── schemas.py
    ├── llm_client.py
    ├── report_builder.py
    └── utils.py
```

---

## 8. Synthetic monitoring data

Для MVP нужно сгенерировать синтетические агрегированные данные за 60 дней.

Рекомендуемые процессы:

- `process_monitoring`;
- `model_monitoring`;
- `optimizer_monitoring`;
- `data_quality_monitoring`.

Рекомендуемые поля:

```text
report_date
report_month
process
product
dpd_bucket
segment
model_name
model_version
optimizer_name
cnt_clients
cnt_scored
cnt_approved_for_communication
cnt_rejected_by_optimizer
reject_share
target_rate
gini
avg_score
median_score
p90_score
high_risk_share
score_missing_rate
feature_missing_rate
empty_feature_vector_share
psi_score
psi_features
communication_call_share
communication_visit_share
communication_sms_share
communication_waiting_share
communication_agency_share
unknown_communication_share
event_type
is_expected_event
```

Допустимые продукты:

```text
cash_loan
credit_card
mortgage
auto_loan
```

Допустимые DPD buckets:

```text
1-30
31-60
61-90
90+
```

Допустимые сегменты:

```text
base
new_high_risk
regular_flow
technical_event
```

---

## 9. Alert objects

После проверок Python должен формировать `alert objects`.

Пример структуры:

```json
{
  "alert_id": "gini_drop_model_monitoring_credit_card_2026_06_15",
  "report_id": "demo_run",
  "process": "model_monitoring",
  "block": "Model quality monitoring",
  "metric": "gini",
  "alert_type": "drop",
  "product": "credit_card",
  "segment": "base",
  "dpd_bucket": "31-60",
  "model_name": "collection_score_v1",
  "model_version": "1.0",
  "current_period": "2026-06-15",
  "previous_period": "2026-06-14",
  "current_value": 0.31,
  "previous_value": 0.42,
  "delta_abs": -0.11,
  "delta_pp": -11.0,
  "delta_rel": -0.262,
  "threshold_abs": -0.05,
  "severity": "critical",
  "cnt_clients": 18500,
  "priority_score": 95.4,
  "python_description": "Gini модели collection_score_v1 снизился с 0.42 до 0.31, падение превышает critical-порог."
}
```

Обязательные поля:

- `alert_id`;
- `report_id`;
- `process`;
- `block`;
- `metric`;
- `alert_type`;
- `product`;
- `segment`;
- `current_value`;
- `previous_value`;
- `delta_abs`;
- `delta_pp`;
- `threshold_abs`;
- `severity`;
- `cnt_clients`;
- `priority_score`;
- `python_description`.

---

## 10. Alert rules

Нужно реализовать базовые проверки.

### Process monitoring

```text
volume_drop:
- warning: падение cnt_clients больше 20%
- critical: падение cnt_clients больше 50%

volume_spike:
- warning: рост cnt_clients больше 30%
- critical: рост cnt_clients больше 70%

product_mix_shift:
- warning: изменение доли продукта больше 10 п.п.
- critical: изменение доли продукта больше 20 п.п.

null_metrics_event:
- warning: доля NULL в ключевых метриках больше 20%
- critical: доля NULL в ключевых метриках больше 50%
```

### Model monitoring

```text
gini_drop:
- warning: падение Gini больше 0.03
- critical: падение Gini больше 0.07

target_rate_shift:
- warning: изменение target_rate больше 2 п.п.
- critical: изменение target_rate больше 5 п.п.

avg_score_shift:
- warning: изменение avg_score больше 0.05
- critical: изменение avg_score больше 0.10

score_distribution_shift:
- warning: PSI score > 0.10
- critical: PSI score > 0.20

high_risk_share_growth:
- warning: рост high_risk_share больше 5 п.п.
- critical: рост high_risk_share больше 10 п.п.
```

### Data quality monitoring

```text
feature_missing_rate_growth:
- warning: рост feature_missing_rate больше 10 п.п.
- critical: рост feature_missing_rate больше 25 п.п.

empty_feature_vector_share_growth:
- warning: рост empty_feature_vector_share больше 2 п.п.
- critical: рост empty_feature_vector_share больше 5 п.п.

score_missing_rate_growth:
- warning: рост score_missing_rate больше 5 п.п.
- critical: рост score_missing_rate больше 15 п.п.
```

### Optimizer monitoring

```text
reject_share_growth:
- warning: рост reject_share больше 10 п.п.
- critical: рост reject_share больше 25 п.п.

approved_for_communication_drop:
- warning: падение cnt_approved_for_communication больше 20%
- critical: падение cnt_approved_for_communication больше 50%

all_channels_rejected_alert:
- critical: reject_share высокий одновременно по call, visit, sms, waiting, agency

communication_mix_shift:
- warning: изменение доли коммуникации больше 10 п.п.
- critical: изменение доли коммуникации больше 25 п.п.
```

---

## 11. Alert grouping

Отдельные `alert objects` нужно группировать в `alert groups`.

Основная группировка:

```text
process + product + segment + dpd_bucket
```

Внутри группы:

- выбрать `main_alert` по максимальному `priority_score`;
- остальные алерты сохранить как `related_alerts`;
- посчитать `group_priority_score`;
- посчитать `alerts_count`;
- посчитать `critical_count`;
- посчитать `warning_count`;
- собрать список `metrics`;
- собрать список `business_zones`.

Пример alert group:

```json
{
  "alert_group_id": "model_monitoring__credit_card__base__31-60",
  "process": "model_monitoring",
  "product": "credit_card",
  "segment": "base",
  "dpd_bucket": "31-60",
  "main_business_zone": "model_quality",
  "main_alert": {
    "metric": "gini",
    "severity": "critical",
    "delta_abs": -0.11,
    "python_description": "Gini модели collection_score_v1 снизился с 0.42 до 0.31."
  },
  "related_alerts": [
    {
      "metric": "target_rate",
      "severity": "warning",
      "delta_pp": 3.2
    },
    {
      "metric": "psi_score",
      "severity": "warning",
      "current_value": 0.14
    }
  ],
  "alerts_count": 3,
  "critical_count": 1,
  "warning_count": 2,
  "group_priority_score": 132.5,
  "business_zones": [
    "model_quality",
    "target_stability",
    "score_distribution"
  ],
  "metrics": [
    "gini",
    "target_rate",
    "psi_score"
  ]
}
```

---

## 12. Business zones

Нужно завести маппинг метрик в бизнесовые зоны.

```python
METRIC_TO_BUSINESS_ZONE = {
    "cnt_clients": "volume",
    "product_share": "portfolio_mix",
    "null_metrics_rate": "technical_availability",

    "gini": "model_quality",
    "target_rate": "target_stability",
    "avg_score": "score_distribution",
    "median_score": "score_distribution",
    "p90_score": "score_distribution",
    "high_risk_share": "portfolio_risk",
    "psi_score": "score_distribution",
    "psi_features": "feature_drift",

    "feature_missing_rate": "data_quality",
    "score_missing_rate": "data_quality",
    "empty_feature_vector_share": "data_quality",

    "reject_share": "optimizer_logic",
    "cnt_approved_for_communication": "optimizer_output",
    "communication_call_share": "communication_mix",
    "communication_visit_share": "communication_mix",
    "communication_sms_share": "communication_mix",
    "communication_waiting_share": "communication_mix",
    "communication_agency_share": "communication_mix",
    "unknown_communication_share": "communication_mapping"
}
```

---

## 13. Priority score

Для ранжирования алертов и alert groups нужно считать `priority_score`.

Упрощенная формула:

```python
priority_score = severity_weight * metric_weight * deviation_strength * volume_weight
```

Где:

```python
SEVERITY_WEIGHT = {
    "info": 1.0,
    "warning": 2.0,
    "critical": 3.0
}
```

Пример весов метрик:

```python
METRIC_WEIGHT = {
    "gini": 1.0,
    "reject_share": 1.0,
    "empty_feature_vector_share": 0.95,
    "feature_missing_rate": 0.9,
    "cnt_clients": 0.85,
    "target_rate": 0.85,
    "avg_score": 0.8,
    "psi_score": 0.8,
    "high_risk_share": 0.75,
    "product_share": 0.7,
    "communication_waiting_share": 0.65,
    "unknown_communication_share": 0.65
}
```

`deviation_strength`:

```python
abs(delta_abs) / abs(threshold_abs)
```

`volume_weight`:

```python
log1p(cnt_clients)
```

---

## 14. RAG documentation

В демостенде RAG-документация лежит в Markdown и имитирует Confluence.

Структура:

```text
docs/
  common/
    metrics_dictionary.md
    monitoring_rules.md
    known_events.md

  process_monitoring/
    process_description.md
    anomaly_playbook.md

  model_monitoring/
    process_description.md
    anomaly_playbook.md

  optimizer_monitoring/
    process_description.md
    anomaly_playbook.md

  data_quality_monitoring/
    process_description.md
    anomaly_playbook.md
```

Логика retrieval:

```text
Если process = model_monitoring:
искать только в docs/common и docs/model_monitoring.

Если process = optimizer_monitoring:
искать только в docs/common и docs/optimizer_monitoring.
```

Функции в `rag.py`:

```python
load_documents()
split_documents()
retrieve_context(query: str, process: str, top_k: int = 3)
```

Запрос для RAG должен строиться из:

```text
process
metric
alert_type
business_zones
main_alert python_description
related metrics
event_type
is_expected_event
```

---

## 15. LLM logic

Для MVP сначала нужен `MockLLMClient`, потом можно подключить `GigaChatClient`.

Интерфейс клиента:

```python
class BaseLLMClient:
    def generate_alert_group_comment(self, prompt: str) -> dict:
        ...

    def generate_final_summary(self, prompt: str) -> dict:
        ...
```

Сначала реализовать:

```python
MockLLMClient
```

Потом добавить:

```python
GigaChatClient
```

Если GigaChat API недоступен, pipeline должен уметь работать через `MockLLMClient`.

---

## 16. LLM output validation

LLM должна возвращать JSON.

Ответы нужно валидировать через Pydantic.

Не использовать регулярные выражения как основной способ обработки ответа.

Пайплайн:

```text
LLM raw answer
        ↓
json.loads
        ↓
Pydantic validation
        ↓
если ошибка — repair prompt
        ↓
validated object
        ↓
сохранение и генерация отчетов
```

Regex можно использовать только как fallback, если модель обернула JSON в markdown-блок.

---

## 17. Schema: alert group comment

Пример ожидаемого JSON от LLM по alert group:

```json
{
  "short_title": "Критичный рост отказов оптимизатора по коммуникациям",
  "short_conclusion": "В мониторинге оптимизатора выявлен массовый рост отказов по коммуникациям, что может указывать на сбой бизнес-логики или ограничений.",
  "facts": [
    "Reject share вырос с 18% до 72%.",
    "Количество клиентов, одобренных для коммуникации, снизилось на 58%.",
    "Отклонение наблюдается по нескольким каналам коммуникации."
  ],
  "business_interpretation": "Массовый отказ по всем коммуникациям не похож на локальный сдвиг одного канала. Это может быть связано с изменением правил оптимизатора, бюджетными ограничениями или ошибкой в справочниках коммуникаций.",
  "possible_causes": [
    "изменение правил бизнес-оптимизатора",
    "некорректное бюджетное ограничение",
    "ошибка в справочнике коммуникаций",
    "проблема во входных признаках оптимизатора"
  ],
  "recommended_checks": [
    "проверить последнюю версию правил оптимизатора",
    "проверить бюджетные ограничения",
    "проверить справочники коммуникаций",
    "проверить входные признаки и fallback-логику"
  ],
  "event_classification": "potential_incident",
  "risk_level": "high",
  "confidence": "medium"
}
```

Поле `event_classification` должно принимать значения:

```text
expected_event
expected_process_feature
potential_incident
needs_manual_review
```

---

## 18. Schema: final summary

Пример ожидаемого JSON финального summary:

```json
{
  "overall_status": "warning",
  "main_problem_area": "optimizer_monitoring / communication decisions",
  "executive_summary": "В текущем мониторинге выявлено несколько отклонений. Часть из них объясняется ожидаемыми процессными событиями, например ЕДН и неритмичным поступлением портфеля credit_card. При этом массовый рост отказов оптимизатора и падение Gini модели требуют ручной проверки.",
  "key_findings": [
    "ЕДН вызвал NULL/0 в части метрик, событие ожидаемо по документации.",
    "Всплеск credit_card похож на регулярную особенность загрузки портфеля.",
    "Gini модели снизился ниже critical-порога.",
    "Reject share оптимизатора резко вырос по всем коммуникациям."
  ],
  "expected_events": [
    "ЕДН",
    "неритмичный поток credit_card"
  ],
  "potential_incidents": [
    "падение Gini модели",
    "пустой feature vector",
    "массовый рост отказов оптимизатора"
  ],
  "priority_checks": [
    "проверить качество входных признаков модели",
    "проверить target_rate и PSI score",
    "проверить правила и бюджетные ограничения оптимизатора",
    "проверить справочники коммуникаций"
  ],
  "manager_summary": "Мониторинг содержит как ожидаемые отклонения, так и потенциальные инциденты. Основной фокус ручной проверки — качество модели, входные признаки и логика оптимизатора."
}
```

---

## 19. Prompt for alert group comment

Промпт должен строиться примерно так:

```text
Ты AI-аналитик мониторинга процессов Collection.

Твоя задача — объяснить группу алертов бизнесовым языком.
Отделяй факты от гипотез.
Не выдумывай причин, если они не следуют из данных.
Используй только переданные факты и документацию.
Верни ответ строго в JSON без markdown и текста вокруг.

Важно:
Не каждое отклонение является инцидентом.
Если документация объясняет событие как ожидаемое, классифицируй его как expected_event или expected_process_feature.
Если отклонение похоже на сбой, классифицируй его как potential_incident.
Если данных недостаточно, классифицируй как needs_manual_review.

Документация:
{rag_context}

Группа алертов:
{alert_group_json}

Схема ответа:
{
  "short_title": "string",
  "short_conclusion": "string",
  "facts": ["string"],
  "business_interpretation": "string",
  "possible_causes": ["string"],
  "recommended_checks": ["string"],
  "event_classification": "expected_event | expected_process_feature | potential_incident | needs_manual_review",
  "risk_level": "low | medium | high",
  "confidence": "low | medium | high"
}
```

---

## 20. Prompt for final summary

Финальный промпт должен получать:

- общую статистику мониторинга;
- top-3/top-5 alert groups;
- комментарии LLM по этим группам;
- общий RAG-контекст по процессам;
- задачу сформировать итоговое заключение.

Пример:

```text
Ты AI-аналитик мониторинга процессов Collection.

Твоя задача — сформировать итоговое заключение по мониторингу в целом.
Не пересказывай каждый алерт отдельно.
Найди общую картину, связи между алертами и главные зоны внимания.
Отделяй факты от гипотез.
Не выдумывай причин, если они не следуют из данных.
Верни ответ строго в JSON без markdown и текста вокруг.

Важно:
Раздели ожидаемые события и потенциальные инциденты.
Ожидаемые события не нужно эскалировать как проблему, но нужно указать, что их стоит исключить из регулярной оценки динамики.
Потенциальные инциденты нужно вынести в priority_checks.

Общая статистика мониторинга:
{monitoring_stats}

Top alert groups:
{top_alert_groups}

Комментарии по top alert groups:
{alert_group_comments}

Документация:
{rag_context}

Схема ответа:
{
  "overall_status": "ok | warning | critical",
  "main_problem_area": "string",
  "executive_summary": "string",
  "key_findings": ["string"],
  "expected_events": ["string"],
  "potential_incidents": ["string"],
  "priority_checks": ["string"],
  "manager_summary": "string"
}
```

---

## 21. Human report

Нужно сформировать `human_report.md`.

Структура:

```text
# Collection Monitoring Report

## 1. Общая статистика
- период;
- количество проверок;
- количество alert groups;
- critical;
- warning;
- OK;
- expected events;
- potential incidents.

## 2. Top alert groups
Для каждой top-группы:
- процесс;
- продукт;
- сегмент;
- severity;
- event_classification;
- main alert;
- related alerts;
- комментарий LLM;
- что проверить.

## 3. Все проверки
Для каждой проверки:
- если алерта нет: "Отклонений не выявлено";
- если алерт есть: факты + ссылка на комментарий / краткий комментарий.

## 4. Ожидаемые события
Например:
- ЕДН;
- неритмичный поток credit_card.

## 5. Потенциальные инциденты
Например:
- падение Gini;
- пустой feature vector;
- массовый рост отказов оптимизатора.

## 6. Финальное заключение
- executive_summary;
- key_findings;
- priority_checks;
- manager_summary.
```

---

## 22. Run archive

На каждый запуск сохранять отдельную папку:

```text
outputs/runs/{run_id}/
```

Внутри:

```text
monitoring_data.csv
alert_objects.json
alert_groups.json
alert_group_comments.json
final_summary.json
history_summary.json
human_report.md
```

---

## 23. history_summary.json

Для MVP historical RAG не обязателен.

Но после каждого запуска нужно сохранять компактное summary для будущего развития.

Пример:

```json
{
  "report_id": "demo_run",
  "period": "2026-06",
  "overall_status": "warning",
  "main_problem_area": "optimizer_monitoring / communication decisions",
  "expected_events": [
    "ЕДН",
    "неритмичный поток credit_card"
  ],
  "potential_incidents": [
    "падение Gini модели",
    "пустой feature vector",
    "массовый рост отказов оптимизатора"
  ],
  "main_alert_groups": [
    {
      "alert_group_id": "optimizer_monitoring__all_products__base__all_dpd",
      "short_title": "Критичный рост отказов оптимизатора по коммуникациям",
      "severity": "critical",
      "metrics": ["reject_share", "cnt_approved_for_communication"]
    }
  ],
  "manager_summary": "Мониторинг содержит как ожидаемые процессные события, так и потенциальные инциденты. Основной фокус ручной проверки — качество модели, входные признаки и логика оптимизатора.",
  "priority_checks": [
    "проверить качество входных признаков модели",
    "проверить target_rate и PSI score",
    "проверить правила и бюджетные ограничения оптимизатора",
    "проверить справочники коммуникаций"
  ]
}
```

---

## 24. Save points

Проект нужно делать по точкам сохранения.

### Save Point 1 — расчетный слой

Реализовать:

- `generate_demo_data.py`;
- `detect_anomalies.py`;
- `group_alerts.py`.

Выход:

- `monitoring_data.csv`;
- `alert_objects.json`;
- `alert_groups.json`.

### Save Point 2 — Mock LLM

Реализовать:

- `schemas.py`;
- `prompts.py`;
- `llm_client.py` с `MockLLMClient`.

Выход:

- `alert_group_comments.json`;
- `final_summary.json`.

### Save Point 3 — Human report

Реализовать:

- `report_builder.py`.

Выход:

- `human_report.md`.

### Save Point 4 — Documentation RAG

Реализовать:

- `docs/*.md`;
- `rag.py`;
- подключение RAG-контекста к промптам.

### Save Point 5 — GigaChat API

Реализовать:

- `GigaChatClient`;
- fallback на `MockLLMClient`;
- валидацию JSON-ответов.

### Save Point 6 — polish

Добавить:

- красивые демо-данные;
- понятные комментарии;
- финальный отчет;
- возможно Streamlit UI, если останется время.

---

## 25. Commands

Желаемые команды запуска:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

После запуска должна появиться папка:

```text
outputs/runs/demo_run/
```

С файлами:

```text
monitoring_data.csv
alert_objects.json
alert_groups.json
alert_group_comments.json
final_summary.json
history_summary.json
human_report.md
```

---

## 26. Development rules for Codex/GigaCode

При разработке соблюдать правила:

1. Не использовать реальные клиентские данные.
2. Не усложнять архитектуру без необходимости.
3. Сначала сделать рабочий pipeline с `MockLLMClient`.
4. Только после этого подключать `GigaChatClient`.
5. Все ответы LLM должны валидироваться через Pydantic.
6. Не использовать регулярные выражения как основной способ парсинга LLM-ответов.
7. Не делать production-ready интеграции, если они не нужны для MVP.
8. Код должен быть простым, читаемым и модульным.
9. Каждая функция должна иметь понятную ответственность.
10. На каждом save point проект должен запускаться и давать результат.
11. Если есть выбор между простой рабочей реализацией и сложной архитектурой, выбирать простую рабочую реализацию.

---

## 27. Suggested requirements

Минимальный набор библиотек:

```text
pandas
numpy
pydantic
scikit-learn
matplotlib
plotly
python-dotenv
requests
```

Опционально:

```text
streamlit
gigachat
```

---

## 28. Expected demo result

После запуска pipeline пользователь должен увидеть:

1. Сгенерированные синтетические данные мониторинга.
2. Найденные alert objects.
3. Сгруппированные alert groups.
4. LLM-комментарии по top alert groups.
5. Разделение отклонений на:
   - ожидаемые события;
   - особенности процесса;
   - потенциальные инциденты;
   - зоны для ручной проверки.
6. Финальное summary по мониторингу.
7. Human report, который можно показать на хакатоне.

Ключевая демо-идея:

> Раньше аналитик вручную смотрел большой мониторинг. Теперь агент сам выделяет проблемные зоны, объясняет их с учетом документации и помогает понять, где ожидаемое событие, а где потенциальный инцидент.
