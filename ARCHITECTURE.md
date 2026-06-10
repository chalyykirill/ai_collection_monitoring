# Architecture

Collection Monitoring Agent построен как последовательный и контролируемый
pipeline. Расчет фактов выполняется Python-кодом, а GigaChat отвечает за
классификацию, выбор диагностических инструментов и бизнес-интерпретацию.

```text
Synthetic monitoring data
        ↓
Alert detection and grouping
        ↓
Documentation retrieval
        ↓
LLM comments
        ↓
Controlled investigation
        ↓
Final summary
        ↓
HTML report
```

## Components

### Data generator

`src/generate_demo_data.py`

Создает синтетический агрегированный мониторинг процессов, моделей,
оптимизатора и качества данных. В датасет заложены шесть демонстрационных
сценариев. Реальные клиентские данные не используются.

### Alert detector

`src/detect_anomalies.py`

Сравнивает текущие значения с предыдущим периодом, применяет фиксированные
правила и пороги, формирует `alert_objects.json`. Описание алерта содержит
только наблюдаемый факт без LLM-гипотез.

### Alert grouper

`src/group_alerts.py`

Добавляет business zones и объяснимый `priority_score`, объединяет связанные
алерты и выбирает `main_alert`. Результат сохраняется в
`alert_groups.json`.

### Mini-RAG

`src/rag.py`

Загружает Markdown-документы из `docs/common/` и каталога соответствующего
процесса, делит их на фрагменты и выполняет TF-IDF retrieval. Найденный
контекст и источники сохраняются в `retrieved_contexts.json`.

### Alert Commentator

`src/llm_client.py`, `src/prompts.py`

Получает alert group и RAG-контекст. Возвращает структурированный комментарий,
факты, бизнес-интерпретацию, рекомендуемые проверки и классификацию события.

### Investigation Agent

`src/investigation_agent.py`

Реализует конечный workflow из двух LLM-запросов на группу:

1. выбор diagnostic tools;
2. интерпретация результатов выполненных tools.

Бесконечного agent loop и произвольного исполнения кода нет.

### Diagnostic tools

`src/diagnostic_tools.py`

Детерминированные Python-функции проверяют календарь событий, объем,
продуктовый и коммуникационный микс, target rate, PSI, missing rates,
распределение score и поведение оптимизатора. Доступные функции собраны в
`TOOL_REGISTRY`.

### Final Summarizer

`run_final_summary.py`, `src/llm_client.py`

Объединяет комментарии и investigation reports в executive summary.
Ожидаемые события и потенциальные инциденты выводятся раздельно. Покрытие
всех групп дополнительно проверяется детерминированно.

### Report builder

`src/charts.py`, `src/report_builder.py`

Строит PNG-графики и формирует `human_report.html` со статистикой,
комментариями, RAG-источниками, результатами tools, гипотезами и итоговым
резюме.

## Prompt architecture

Все LLM-ответы возвращаются как JSON и валидируются Pydantic-схемами.

1. **Alert Commentator Prompt** — первичная интерпретация и классификация.
2. **Investigation Planner Prompt** — выбор tools из переданного whitelist.
3. **Investigation Summarizer Prompt** — интерпретация tool results.
4. **Final Summarizer Prompt** — executive summary всего мониторинга.
5. **JSON Repair Prompt** — исправление структуры невалидного JSON.
6. **Language Repair Prompt** — перевод человекочитаемых полей на русский без
   изменения ключей и технических идентификаторов.

## Agent workflow

```text
alert_group + comment + RAG
        ↓
planner prompt
        ↓
tool plan JSON
        ↓
whitelist validation
        ↓
Python diagnostic tools
        ↓
tool results
        ↓
summarizer prompt
        ↓
investigation report
```

Planner может выбрать не более пяти инструментов. Python удаляет неизвестные
tools и дубли, затем вызывает функции из `TOOL_REGISTRY`. Summarizer получает
готовые evidence и не исполняет инструменты самостоятельно.

## Safety and control

- нет произвольного исполнения кода;
- доступны только tools из whitelist;
- расчеты и пороги остаются в Python;
- все LLM-ответы валидируются через Pydantic;
- при нарушении схемы используется JSON repair;
- английские человекочитаемые фразы исправляются language repair;
- semantic guards устраняют противоречивые трактовки expected events;
- `run_full_demo.py` выполняет deterministic audit итоговых артефактов.

## Run sequence

```text
run_pipeline.py
run_gigachat_comments.py
run_investigations.py
run_final_summary.py
run_build_report.py
```

`run_full_demo.py` последовательно запускает все этапы и проверяет готовность
результата к демонстрации.
