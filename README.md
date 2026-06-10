# Collection Monitoring Agent

AI-агент для анализа мониторинга процессов, моделей, оптимизаторов и качества данных в Collection.

Проект для хакатона **«Агенты в Collection»**. MVP работает только на синтетических агрегированных данных и показывает, как агент помогает аналитику быстрее разбирать мониторинг: находит алерты, объясняет их с учетом документации, запускает диагностические проверки и формирует итоговое резюме.

## 1. Главный принцип

**Python считает факты. LLM объясняет факты и выбирает диагностику.**

LLM не считает метрики и не ищет отклонения по графикам. Python заранее формирует агрегаты, `alert objects`, `alert groups`, `priority score` и `evidence`.

## 2. Архитектура

```text
Synthetic monitoring data
        ↓
Python monitoring engine
        ↓
Alert objects
        ↓
Alert groups + priority
        ↓
RAG documentation context
        ↓
1. Alert Commentator
        ↓
2. Investigation Agent + diagnostic tools
        ↓
3. Final Summarizer
        ↓
Human report + run archive
```

## 3. Компоненты

### 3.1 Python monitoring engine

Делает:

- генерирует синтетические агрегированные данные;
- считает метрики;
- сравнивает текущий период с предыдущим;
- формирует `alert objects`;
- группирует связанные алерты в `alert groups`;
- считает `priority_score`;
- строит графики для отчета;
- выполняет диагностические функции для Investigation Agent.

### 3.2 Alert Commentator

LLM-компонент.

Получает:

- `alert_group`;
- `python_description`;
- `related_alerts`;
- RAG-контекст по процессу и типу события.

Делает:

- объясняет alert group бизнесовым языком;
- классифицирует событие:
  - `expected_event`;
  - `expected_process_feature`;
  - `potential_incident`;
  - `needs_manual_review`;
- формирует первичные выводы и recommended checks.

Выход: `alert_group_comments.json`.

### 3.3 Investigation Agent

LLM-компонент с controlled tool calling.

Получает:

- `alert_group`;
- комментарий Alert Commentator;
- RAG-контекст;
- список разрешенных diagnostic tools.

Делает:

- выбирает релевантные диагностические проверки;
- использует только whitelist tools;
- максимум 5 tools на alert group;
- Python выполняет выбранные tools;
- агент получает tool results и формирует root cause hypothesis.

Выход: `investigation_reports.json`.

### 3.4 Final Summarizer

LLM-компонент.

Получает:

- monitoring stats;
- top alert groups;
- alert group comments;
- investigation reports;
- короткий RAG-контекст.

Делает:

- формирует executive summary;
- разделяет ожидаемые события и потенциальные инциденты;
- выделяет root cause hypotheses;
- формирует priority checks и manager summary.

Выход: `final_summary.json`.

## 4. Главные демо-сценарии

Синтетические данные должны содержать 6 сценариев.

### 4.1 ЕДН — единый день недоступности банка

Метрики становятся NULL/0 из-за технологического события.  
Ожидаемый вывод: это `expected_event`, если дата совпадает с календарем ЕДН.

### 4.2 Неритмичное поступление credit_card

В отдельный день резко растет поток кредитных карт.  
Ожидаемый вывод: это `expected_process_feature`, если соответствует документации по загрузке портфеля.

### 4.3 Падение Gini модели

Gini модели падает ниже порога.  
Ожидаемый вывод: `potential_incident`, нужно проверить target rate, PSI, score distribution, состав потока.

### 4.4 Пустой feature vector

Растет missing rate / empty vector share, меняется avg_score.  
Ожидаемый вывод: `potential_incident`, вероятна проблема качества данных.

### 4.5 Новый рискованный сегмент

Растет avg_score, high_risk_share, target_rate, PSI.  
Ожидаемый вывод: изменение состава потока, проверить продуктовый/DPD/сегментный микс.

### 4.6 Массовые отказы оптимизатора

Растет reject_share, падает approved_for_communication.  
Ожидаемый вывод: `potential_incident`, проверить правила оптимизатора, бюджеты, справочники и входные признаки.

## 5. Структура проекта

```text
collection_monitoring_agent/
├── README.md
├── AGENTS.md
├── requirements.txt
├── run_pipeline.py
│
├── docs/
│   ├── common/
│   │   ├── known_events.md
│   │   ├── metrics_dictionary.md
│   │   └── monitoring_rules.md
│   ├── process_monitoring/
│   ├── model_monitoring/
│   ├── optimizer_monitoring/
│   └── data_quality_monitoring/
│
├── outputs/
│   └── runs/
│       └── demo_run/
│           ├── monitoring_data.csv
│           ├── alert_objects.json
│           ├── alert_groups.json
│           ├── alert_group_comments.json
│           ├── investigation_reports.json
│           ├── final_summary.json
│           ├── history_summary.json
│           ├── human_report.html
│           └── charts/
│
└── src/
    ├── generate_demo_data.py
    ├── detect_anomalies.py
    ├── group_alerts.py
    ├── rag.py
    ├── prompts.py
    ├── schemas.py
    ├── llm_client.py
    ├── diagnostic_tools.py
    ├── investigation_agent.py
    ├── charts.py
    ├── report_builder.py
    └── utils.py
```

## 6. Synthetic monitoring data

Рекомендуемые процессы:

- `process_monitoring`;
- `model_monitoring`;
- `optimizer_monitoring`;
- `data_quality_monitoring`.

Ключевые поля:

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

## 7. Alert object

Каждый alert object должен содержать:

```text
alert_id
report_id
process
block
metric
alert_type
product
dpd_bucket
segment
model_name
model_version
optimizer_name
current_date
previous_date
current_value
previous_value
delta_abs
delta_rel
threshold_abs
severity
cnt_clients
event_type
is_expected_event
python_description
priority_score
```

## 8. Alert group

Группировка:

```text
process + product + dpd_bucket + segment + model_name + optimizer_name + event_type
```

Каждая alert group содержит:

```text
alert_group_id
process
product
dpd_bucket
segment
event_type
is_expected_event
main_alert
related_alerts
alerts_count
critical_count
warning_count
metrics
business_zones
group_priority_score
```

## 9. RAG

RAG-документация имитирует Confluence.

Используется:

- в Alert Commentator — обязательно;
- в Investigation Agent — обязательно;
- в Final Summarizer — кратко, только релевантные выдержки.

Retrieval должен ограничиваться процессом:

```text
docs/common + docs/{process}
```

Не искать по всей документации без фильтра по process.

## 10. Diagnostic tools

Investigation Agent может выбирать только whitelist tools:

```text
check_known_event_calendar
check_product_mix_shift
check_target_rate_shift
check_psi_shift
check_missing_rate
check_empty_feature_vector
check_score_distribution
check_optimizer_reject_share
check_communication_mix
check_model_version_change
```

Каждый tool возвращает JSON:

```json
{
  "tool_name": "...",
  "status": "ok | warning | critical",
  "finding": "...",
  "evidence": {},
  "supports_hypothesis": true
}
```

## 11. LLM output format

Все LLM-ответы должны быть JSON и валидироваться через Pydantic.

Pipeline:

```text
raw LLM response
    ↓
extract JSON
    ↓
json.loads
    ↓
Pydantic validation
    ↓
repair prompt if invalid
    ↓
validated object
```

Regex разрешен только как fallback для извлечения JSON-блока.

## 12. Output-файлы

После запуска:

```bash
python run_pipeline.py
```

должны появиться:

```text
outputs/runs/demo_run/monitoring_data.csv
outputs/runs/demo_run/alert_objects.json
outputs/runs/demo_run/alert_groups.json
outputs/runs/demo_run/alert_group_comments.json
outputs/runs/demo_run/investigation_reports.json
outputs/runs/demo_run/final_summary.json
outputs/runs/demo_run/history_summary.json
outputs/runs/demo_run/human_report.html
outputs/runs/demo_run/charts/
```

## 13. Human report

`human_report.html` должен содержать:

- executive summary;
- monitoring statistics;
- список alert groups;
- графики по каждой alert group;
- комментарий Alert Commentator;
- investigation results;
- root cause hypothesis;
- priority checks;
- manager summary.

## 14. Ограничения MVP

Не делать:

- реальные клиентские данные;
- принятие решений по клиентам;
- production-интеграцию с Confluence;
- исторический RAG по прошлым мониторингам;
- бесконечные agent loops;
- произвольное выполнение кода LLM;
- сложный UI, если не готов основной pipeline.

## 15. Save points

### Save Point 1

Synthetic data + alert objects + alert groups.

### Save Point 2

GigaChat comments + Pydantic validation + charts + human report.

### Save Point 3

RAG documentation.

### Save Point 4

Investigation Agent + diagnostic tools.

### Save Point 5

Final Summarizer + final report polish.

## 16. Demo result

Финальное демо должно показать:

1. Python нашел 6 реалистичных alert groups.
2. LLM объяснила каждую группу с учетом документации.
3. Investigation Agent выбрал проверки и собрал evidence.
4. Система отличила expected events от potential incidents.
5. Итоговый отчет содержит графики, ход расследования и executive summary.
