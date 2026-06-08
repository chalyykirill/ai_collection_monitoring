# AGENTS.md — инструкции для Codex/GigaCode

Этот файл содержит постоянные инструкции для AI coding agent при работе с проектом **Collection Monitoring Agent**.

Проект создается для хакатона **"Агенты в Collection"**. Главная цель — быстро собрать демонстрационный MVP, который работает на синтетических агрегированных данных и показывает агентный анализ мониторинга процессов, моделей, оптимизаторов и качества данных в Collection.

---

## 1. Роль Codex в проекте

Codex/GigaCode используется как coding agent.

Твоя задача:

- писать простой и запускаемый Python-код;
- реализовывать модули по save points;
- не усложнять архитектуру без необходимости;
- сохранять промежуточные результаты в файлы;
- помогать быстро довести MVP до демонстрации.

Codex не должен самостоятельно переизобретать продуктовую концепцию. Основная концепция проекта описана в `README.md`.

---

## 2. Главный принцип проекта

**Python считает факты. LLM объясняет факты бизнесовым языком с учетом документации.**

Не нужно заставлять LLM искать аномалии в графиках или сырых таблицах. Python должен заранее посчитать агрегаты, проверки, алерты, приоритеты и подготовить компактный контекст.

---

## 3. Строгие ограничения

Нельзя:

- усложнять код фреймворками без необходимости;
- ломать уже работающие save points.

В MVP используются только синтетические агрегированные данные.

---

## 4. Целевой pipeline MVP

Реализуй проект как последовательный pipeline:

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

## 5. Save points

Работай по точкам сохранения. На каждом save point проект должен запускаться и давать полезный результат.

### Save Point 1 — расчетный слой без LLM

Реализовать:

- `src/generate_demo_data.py`
- `src/detect_anomalies.py`
- `src/group_alerts.py`
- `src/utils.py`
- `run_pipeline.py`

На выходе:

- `outputs/runs/demo_run/monitoring_data.csv`
- `outputs/runs/demo_run/alert_objects.json`
- `outputs/runs/demo_run/alert_groups.json`

### Save Point 2 — Mock LLM

Реализовать:

- `src/schemas.py`
- `src/prompts.py`
- `src/llm_client.py`

Добавить `MockLLMClient`, который возвращает валидный JSON.

На выходе:

- `outputs/runs/demo_run/alert_group_comments.json`
- `outputs/runs/demo_run/final_summary.json`

### Save Point 3 — Human report

Реализовать:

- `src/report_builder.py`

На выходе:

- `outputs/runs/demo_run/human_report.md`

### Save Point 4 — Documentation RAG

Реализовать:

- `docs/**/*.md`
- `src/rag.py`

Для MVP использовать простой retrieval по Markdown-документам.

### Save Point 5 — GigaChat API

Добавить реальный `GigaChatClient`, но сохранить fallback на `MockLLMClient`.

Если API недоступен, pipeline все равно должен работать через mock.

### Save Point 6 — polish

Добавить улучшения только после работающего MVP:

- более красивый отчет;
- больше графиков;
- более аккуратные demo docs;
- Streamlit UI, если останется время.

---

## 6. Демо-кейсы, которые должны быть зашиты в данные

Synthetic data должны отражать реалистичные кейсы мониторинга.

Обязательные сценарии:

1. **ЕДН — единый день недоступности банка**
   - В один день часть метрик становится `NULL` или `0`.
   - Это ожидаемое технологическое событие.
   - Агент должен объяснить, что это не деградация процесса, если дата совпадает с календарем ЕДН.

2. **Неритмичное поступление портфеля кредитных карт**
   - У продукта `credit_card` есть всплески объема и доли в потоке.
   - Агент должен объяснить, что это может быть нормальной особенностью процесса загрузки.

3. **Падение Gini модели**
   - У модели падает `gini`.
   - Агент должен рекомендовать проверить target rate, PSI, score distribution, признаки и состав потока.

4. **Пустой feature vector на входе модели**
   - Растет `empty_feature_vector_share` или `feature_missing_rate`.
   - Может резко измениться `avg_score`.
   - Агент должен связать это с качеством данных, а не с реальным ростом риска.

5. **Новый рискованный сегмент в потоке**
   - Растет `avg_score`, `high_risk_share`, `target_rate`.
   - Агент должен предложить проверить сегментный, продуктовый и DPD-микс.

6. **Бизнес-оптимизатор начал делать отказы по всем коммуникациям**
   - Растет `reject_share` / `no_action_share`.
   - Падает `cnt_approved_for_communication`.
   - Агент должен трактовать это как потенциально критичный сбой бизнес-логики, бюджета или справочников.

---

## 7. Структура данных

Synthetic monitoring dataset должен быть агрегированным.

Базовые поля:

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

Не обязательно заполнять все поля для каждого процесса. Для нерелевантных полей можно использовать `NaN`.

---

## 8. Alert objects

Python должен формировать `alert_objects.json`.

Каждый alert object должен содержать:

```text
alert_id
report_id
process
block
metric
alert_type
segment
dpd_bucket
product
model_name
optimizer_name
current_period
previous_period
current_value
previous_value
delta_abs
delta_pp
delta_rel
threshold_abs
severity
cnt_clients
priority_score
python_description
is_expected_event_candidate
```

`python_description` должен быть коротким человеческим описанием факта, без бизнесовых гипотез.

Пример:

```text
Среднее значение Gini модели collection_score_v1 снизилось с 0.42 до 0.34, отклонение -0.08 превышает warning-порог.
```

---

## 9. Alert groups

Python должен формировать `alert_groups.json`.

Группировка по умолчанию:

```text
process + product + dpd_bucket + segment
```

Если поле нерелевантно, использовать значение `all`.

Внутри группы:

- `main_alert` = alert с максимальным `priority_score`;
- `related_alerts` = остальные alerts группы;
- `group_priority_score` = сумма или максимум priority score;
- `critical_count`;
- `warning_count`;
- `metrics`;
- `business_zones`.

---

## 10. Business zones

Используй маппинг метрик в бизнесовые зоны:

```python
METRIC_TO_BUSINESS_ZONE = {
    "cnt_clients": "volume",
    "cnt_scored": "volume",
    "target_rate": "target_stability",
    "gini": "model_quality",
    "avg_score": "score_distribution",
    "median_score": "score_distribution",
    "p90_score": "score_distribution",
    "high_risk_share": "score_distribution",
    "psi_score": "portfolio_drift",
    "psi_features": "feature_drift",
    "score_missing_rate": "data_quality",
    "feature_missing_rate": "data_quality",
    "empty_feature_vector_share": "data_quality",
    "reject_share": "optimizer_logic",
    "cnt_rejected_by_optimizer": "optimizer_logic",
    "cnt_approved_for_communication": "optimizer_logic",
    "communication_call_share": "communication_mix",
    "communication_visit_share": "communication_mix",
    "communication_sms_share": "communication_mix",
    "communication_waiting_share": "communication_mix",
    "communication_agency_share": "communication_mix",
    "unknown_communication_share": "data_quality"
}
```

---

## 11. Priority score

Для ранжирования alert objects и alert groups использовать простую объяснимую формулу:

```python
priority_score = severity_weight * metric_weight * deviation_strength * volume_weight
```

Где:

- `severity_weight`: `info=1`, `warning=2`, `critical=3`;
- `metric_weight`: задается словарем по важности метрики;
- `deviation_strength`: насколько отклонение превышает порог;
- `volume_weight`: `log1p(cnt_clients)`.

Не усложнять формулу без необходимости.

---

## 12. RAG-документация

Markdown-документы имитируют Confluence.

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

Retrieval должен искать только в:

```text
docs/common/ + docs/{process}/
```

Не искать по всем документам подряд, если известен process.

---

## 13. LLM output

LLM должна возвращать только JSON.

Не принимать свободный текст как финальный формат.

Все ответы LLM валидировать через Pydantic.

Пайплайн:

```text
raw LLM response
    ↓
json.loads
    ↓
Pydantic validation
    ↓
repair prompt при ошибке
    ↓
validated object
```

Regex можно использовать только как fallback для извлечения JSON из markdown-блока.

---

## 14. Mock first

Сначала реализовать `MockLLMClient`.

Реальный `GigaChatClient` добавлять только после того, как pipeline работает через mock.

Требование:

```text
python run_pipeline.py
```

должен работать даже без API-ключей.

---

## 15. Output archive

Каждый запуск должен сохраняться в отдельную папку:

```text
outputs/runs/{run_id}/
```

Для demo использовать:

```text
outputs/runs/demo_run/
```

Обязательные файлы:

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

## 16. Human report

`human_report.md` должен быть понятен человеку.

Структура:

```text
# Collection Monitoring Report

## 1. Общая статистика
- период;
- количество проверок;
- количество алертов;
- количество alert groups;
- critical/warning/ok.

## 2. Top alert groups
- процесс;
- сегмент;
- main alert;
- related alerts;
- комментарий LLM;
- что проверить.

## 3. Все проверки
- графики по агрегатам
- если алерта нет: "Отклонений не выявлено";
- если алерт есть: факты + комментарий.

## 4. Финальное заключение
- executive summary;
- key findings;
- priority checks;
- manager summary.
```

---

## 17. Код-стиль

Пиши код так:

- Python 3.10+;
- простые функции с понятной ответственностью;
- type hints там, где это не мешает скорости;
- без лишнего ООП;
- без сложных фреймворков;
- pandas/numpy для данных;
- pydantic для схем;
-  RAG на основе gigachat api;
- matplotlib/plotly только если нужны графики;
- все пути через `pathlib.Path`;
- сохранять JSON с `ensure_ascii=False` и `indent=2`.

---

## 18. Команды запуска

Основная команда:

```bash
python run_pipeline.py
```

Ожидаемый результат:

```text
outputs/runs/demo_run/
```

с полным набором файлов запуска.

Если добавлены тесты:

```bash
pytest
```

Но тесты не обязательны для первого MVP.

---

## 19. Приоритет реализации

Если задача большая, реализуй в таком порядке:

1. `generate_demo_data.py`
2. `detect_anomalies.py`
3. `group_alerts.py`
4. `run_pipeline.py`
5. `schemas.py`
6. `llm_client.py` с mock
7. `prompts.py`
8. `report_builder.py`
9. `rag.py`
10. `GigaChatClient`
11. UI/Streamlit только после всего выше

---

## 20. Как действовать при неопределенности

Если не хватает деталей:

- не останавливай работу;
- делай разумное простое предположение;
- добавляй комментарий `# TODO:`;
- сохраняй решение минимальным;
- не раздувай архитектуру.

Приоритет — рабочий MVP для хакатона, а не идеальная production-система.

---

## 21. Definition of Done для MVP

MVP считается готовым, если команда:

```bash
python run_pipeline.py
```

создает:

```text
outputs/runs/demo_run/monitoring_data.csv
outputs/runs/demo_run/alert_objects.json
outputs/runs/demo_run/alert_groups.json
outputs/runs/demo_run/alert_group_comments.json
outputs/runs/demo_run/final_summary.json
outputs/runs/demo_run/history_summary.json
outputs/runs/demo_run/human_report.md
```

И в `human_report.md` видно:

- ЕДН как ожидаемое технологическое событие;
- неритмичный поток credit_card как ожидаемая особенность;
- падение Gini как потенциальная проблема модели;
- пустой feature vector как data quality incident;
- новый рискованный сегмент как изменение состава потока;
- массовые отказы оптимизатора как критичный инцидент бизнес-логики.

---

## 22. Главная фраза проекта

Раньше аналитик вручную смотрел большой мониторинг.

Теперь агент сам выделяет проблемные зоны, отличает ожидаемые события от инцидентов и формирует бизнесовое резюме.
