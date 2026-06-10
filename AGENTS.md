# AGENTS.md

Инструкции для Codex/GigaCode при разработке проекта **Collection Monitoring Agent**.

## 1. Роль coding agent

Ты senior Python developer.  
Твоя задача — реализовать MVP проекта по README.md.

Не придумывай новую архитектуру без необходимости.  
Следуй save points.  
Каждый этап должен запускаться командой:

```bash
python run_pipeline.py
```

## 2. Главная архитектура

```text
Synthetic monitoring data
    ↓
Python monitoring engine
    ↓
alert objects
    ↓
alert groups + priority
    ↓
Alert Commentator
    ↓
Investigation Agent + diagnostic tools
    ↓
Final Summarizer
    ↓
human report + run archive
```

## 3. Главный принцип

Python считает факты.  
LLM объясняет факты и выбирает диагностику.

LLM не должна:

- считать метрики;
- искать отклонения по графикам;
- исполнять произвольный код;
- принимать решения по клиентам;
- работать с реальными клиентскими данными.

## 4. Ограничения

Запрещено:

- использовать реальные клиентские данные;
- добавлять production-интеграции без запроса;
- строить сложные agent loops;
- делать произвольное tool execution;
- усложнять структуру проекта;
- ломать существующий pipeline;
- удалять output-файлы без необходимости.

Если есть выбор между простой рабочей реализацией и сложной архитектурой — выбирай простую рабочую.

## 5. Save points

### Save Point 1 — расчетный слой

Реализовать:

- `src/generate_demo_data.py`;
- `src/detect_anomalies.py`;
- `src/group_alerts.py`;
- `run_pipeline.py`.

Outputs:

```text
monitoring_data.csv
alert_objects.json
alert_groups.json
```

### Save Point 2 — LLM comments + charts

Реализовать:

- `src/schemas.py`;
- `src/prompts.py`;
- `src/llm_client.py`;
- `src/charts.py`;
- `src/report_builder.py`.

Outputs:

```text
alert_group_comments.json
final_summary.json
human_report.html
charts/
```

Основной режим — реальный LLM client.  
Fallback/mock допустим только если API недоступен.

### Save Point 3 — RAG documentation

Реализовать:

- `docs/common/*`;
- `docs/{process}/*`;
- `src/rag.py`.

Retrieval ограничивать:

```text
docs/common + docs/{process}
```

### Save Point 4 — Investigation Agent

Реализовать:

- `src/diagnostic_tools.py`;
- `src/investigation_agent.py`;
- `src/investigation_prompts.py`;
- `src/investigation_schemas.py`.

Outputs:

```text
investigation_reports.json
```

### Save Point 5 — final report polish

Обновить:

- `final_summary.json`;
- `history_summary.json`;
- `human_report.html`.

## 6. LLM components

### 6.1 Alert Commentator

Input:

```text
alert_group
python_description
related_alerts
rag_context
```

Output JSON:

```text
short_title
short_conclusion
facts
business_interpretation
possible_causes
recommended_checks
event_classification
risk_level
confidence
```

Allowed `event_classification`:

```text
expected_event
expected_process_feature
potential_incident
needs_manual_review
```

### 6.2 Investigation Agent

Input:

```text
alert_group
alert_group_comment
rag_context
available_tools
```

Rules:

- максимум 5 tools на alert group;
- использовать только whitelist tools;
- если `is_expected_event=True`, сначала вызвать `check_known_event_calendar`;
- не запускать лишние проверки, если expected event подтвержден;
- расследовать top-priority groups, а не все подряд.

Output JSON:

```text
alert_group_id
selected_tools
evidence_summary
root_cause_hypothesis
confidence
recommended_actions
needs_manual_review
```

### 6.3 Final Summarizer

Input:

```text
monitoring_stats
top_alert_groups
alert_group_comments
investigation_reports
short_rag_context
```

Output JSON:

```text
overall_status
executive_summary
expected_events
potential_incidents
root_cause_hypotheses
priority_checks
manager_summary
```

## 7. Diagnostic tools whitelist

Разрешенные tools:

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

Каждый tool возвращает dict:

```json
{
  "tool_name": "...",
  "status": "ok | warning | critical",
  "finding": "...",
  "evidence": {},
  "supports_hypothesis": true
}
```

## 8. Pydantic validation

Все ответы LLM валидировать через Pydantic.

Pipeline:

```text
raw response
    ↓
extract JSON
    ↓
json.loads
    ↓
Pydantic model
    ↓
repair prompt if invalid
```

Не парсить свободный текст регулярками как основной способ.

## 9. Demo scenarios

Синтетические данные должны содержать 6 сценариев:

```text
bank_unavailable_day
credit_card_batch_inflow
model_gini_drop
empty_feature_vector
new_high_risk_segment
optimizer_mass_reject
```

Ожидаемые события:

```text
bank_unavailable_day
credit_card_batch_inflow
```

Потенциальные инциденты:

```text
model_gini_drop
empty_feature_vector
new_high_risk_segment
optimizer_mass_reject
```

## 10. Output archive

Все результаты сохранять в:

```text
outputs/runs/demo_run/
```

Ожидаемые файлы:

```text
monitoring_data.csv
alert_objects.json
alert_groups.json
alert_group_comments.json
investigation_reports.json
final_summary.json
history_summary.json
human_report.html
charts/
```

## 11. Report requirements

`human_report.html` должен содержать:

- monitoring statistics;
- графики по alert groups;
- Alert Commentator output;
- Investigation Agent output;
- root cause hypothesis;
- final executive summary;
- разделение expected events / potential incidents.

## 12. Coding style

- Python 3.10+.
- Простые функции.
- Явные имена.
- Минимум глобального состояния.
- Пути через `pathlib.Path`.
- Сохранять JSON с `ensure_ascii=False`, `indent=2`.
- Код должен запускаться локально без ручных правок.
- Если API credentials не заданы, pipeline не должен падать без объяснения.

## 13. Dependencies

Минимум:

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
gigachat
streamlit
```

## 14. Перед завершением задачи

Всегда проверяй:

```bash
python run_pipeline.py
```

И убедись, что появились нужные output-файлы.

В финальном сообщении укажи:

- что реализовано;
- какие файлы созданы/изменены;
- какая команда запуска;
- какие output-файлы появились;
- что осталось на следующий save point.
