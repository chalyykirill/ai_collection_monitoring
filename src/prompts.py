from __future__ import annotations

import json
from typing import Any

from src.schemas import (
    AlertGroupComment,
    FinalSummary,
    InvestigationPlan,
    InvestigationReport,
)


ALERT_COMMENTATOR_EXAMPLES: list[dict[str, Any]] = [
    {
        "input": {
            "alert_group": {
                "alert_group_id": "example_edn",
                "event_type": "bank_unavailable_day",
                "is_expected_event": True,
                "metrics": ["cnt_clients", "null_metrics_rate"],
            },
            "doc_context": (
                "Дата входит в календарь ЕДН. В этот день допустимы нулевые "
                "объемы и NULL в мониторинге."
            ),
        },
        "output": {
            "alert_group_id": "example_edn",
            "short_title": "ЕДН подтвержден календарем",
            "short_conclusion": "Отклонение соответствует ожидаемому событию.",
            "facts": [
                "Объем снизился до нуля.",
                "Документация подтверждает ЕДН на эту дату.",
            ],
            "business_interpretation": (
                "Наблюдаемое отклонение объясняется технологическим событием."
            ),
            "possible_causes": ["Плановый единый день недоступности банка."],
            "recommended_checks": [
                "Проверить восстановление потока после завершения ЕДН."
            ],
            "event_classification": "expected_event",
            "risk_level": "low",
            "confidence": "high",
        },
    },
    {
        "input": {
            "alert_group": {
                "alert_group_id": "example_optimizer",
                "event_type": "optimizer_mass_reject",
                "is_expected_event": False,
                "metrics": [
                    "reject_share",
                    "cnt_approved_for_communication",
                ],
            },
            "doc_context": (
                "Массовый рост отказов не является штатным режимом и требует "
                "проверки правил, бюджетов и справочников."
            ),
        },
        "output": {
            "alert_group_id": "example_optimizer",
            "short_title": "Массовые отказы оптимизатора",
            "short_conclusion": (
                "Наблюдается потенциально критичное отклонение бизнес-логики."
            ),
            "facts": [
                "Доля отказов выросла.",
                "Количество одобренных коммуникаций снизилось.",
            ],
            "business_interpretation": (
                "Оптимизатор ограничивает коммуникации значительно сильнее "
                "обычного."
            ),
            "possible_causes": [
                "Изменение правил или бюджетных ограничений.",
                "Некорректный справочник коммуникаций.",
            ],
            "recommended_checks": [
                "Проверить правила и ограничения оптимизатора.",
                "Проверить входные данные и справочники.",
            ],
            "event_classification": "potential_incident",
            "risk_level": "high",
            "confidence": "high",
        },
    },
]


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _examples_section(examples: list[dict[str, Any]] | None) -> str:
    if not examples:
        return ""
    return f"\n\n# Примеры\n{_json(examples)}"


def _build_prompt(
    *,
    role: str,
    goal: str,
    context: str,
    doc_context: str,
    input_data: dict[str, Any],
    output_rules: str,
    target_schema: dict[str, Any],
    examples: list[dict[str, Any]] | None,
) -> str:
    return (
        f"# Роль\n{role}\n\n"
        f"# Цель\n{goal}\n\n"
        "# Контекст\n"
        f"{context}\n"
        "Используй только переданные входные данные и документацию. "
        "Не придумывай факты, причины, результаты проверок или положения "
        "документации. Отделяй наблюдаемые факты от гипотез. Если данных "
        "недостаточно, используй needs_manual_review там, где это допускает "
        "схема. Проведи внутренний анализ, но не показывай ход рассуждений.\n\n"
        "# Контекст документации\n"
        f"{doc_context.strip() or 'Документация не передана.'}\n\n"
        "# Входные данные\n"
        f"{_json(input_data)}\n\n"
        "# Выходные данные\n"
        f"{output_rules}\n"
        "Верни строго один JSON-объект без markdown-блоков, комментариев и "
        "текста вокруг JSON.\n\n"
        "# Выходная JSON schema\n"
        f"{_json(target_schema)}"
        f"{_examples_section(examples)}"
    )


def build_alert_commentator_prompt(
    alert_group: dict,
    doc_context: str,
    examples: list[dict] | None = None,
) -> str:
    return _build_prompt(
        role=(
            "Ты Alert Commentator, аналитик первичной интерпретации "
            "мониторинга Collection."
        ),
        goal=(
            "Сформировать краткий бизнесовый комментарий по одной alert group "
            "и классифицировать событие."
        ),
        context=(
            "bank_unavailable_day классифицируй как expected_event только при "
            "подтверждении документацией. credit_card_batch_inflow "
            "классифицируй как expected_process_feature только при таком "
            "подтверждении. model_gini_drop, empty_feature_vector, "
            "new_high_risk_segment и optimizer_mass_reject обычно требуют "
            "potential_incident или needs_manual_review."
        ),
        doc_context=doc_context,
        input_data={"alert_group": alert_group},
        output_rules=(
            "Факты должны следовать из alert group или документации. "
            "possible_causes являются только проверяемыми гипотезами."
        ),
        target_schema=AlertGroupComment.model_json_schema(),
        examples=examples,
    )


def build_investigation_planner_prompt(
    alert_group: dict,
    alert_comment: dict,
    doc_context: str,
    available_tools: list[dict],
    examples: list[dict] | None = None,
) -> str:
    return _build_prompt(
        role=(
            "Ты Investigation Planner, планировщик диагностического "
            "расследования мониторинга Collection."
        ),
        goal=(
            "Выбрать минимальный набор Python diagnostic tools, который "
            "позволит проверить гипотезы по alert group."
        ),
        context=(
            "Выбирай только инструменты из available_tools, не более пяти. "
            "Не вызывай инструменты и не придумывай их результаты. Для "
            "ожидаемого события сначала выбирай проверку календаря или "
            "известного события. Если документация уже подтверждает событие, "
            "допустим минимальный набор tools. Если подходящих tools нет, "
            "верни пустой selected_tools и объясни stop_reason."
        ),
        doc_context=doc_context,
        input_data={
            "alert_group": alert_group,
            "alert_comment": alert_comment,
            "available_tools": available_tools,
        },
        output_rules=(
            "Для каждого выбранного инструмента объясни причину выбора и "
            "какое evidence ожидается. tool_name должен точно совпадать с "
            "именем в whitelist."
        ),
        target_schema=InvestigationPlan.model_json_schema(),
        examples=examples,
    )


def build_investigation_summary_prompt(
    alert_group: dict,
    alert_comment: dict,
    tool_results: list[dict],
    doc_context: str,
    examples: list[dict] | None = None,
) -> str:
    return _build_prompt(
        role=(
            "Ты Investigation Summarizer, аналитик результатов "
            "диагностического расследования Collection."
        ),
        goal=(
            "Свести результаты Python tools в evidence и сформировать "
            "проверяемую гипотезу root cause."
        ),
        context=(
            "Опирайся только на tool_results. Не превращай исходный alert или "
            "документацию в подтвержденное evidence без результата tool. Если "
            "результаты отсутствуют, противоречивы или недостаточны, установи "
            "needs_manual_review=true и снизь confidence."
        ),
        doc_context=doc_context,
        input_data={
            "alert_group": alert_group,
            "alert_comment": alert_comment,
            "tool_results": tool_results,
        },
        output_rules=(
            "evidence_summary должен перечислять только наблюдения из "
            "tool_results. root_cause_hypothesis должна оставаться гипотезой."
        ),
        target_schema=InvestigationReport.model_json_schema(),
        examples=examples,
    )


def build_final_summarizer_prompt(
    monitoring_stats: dict,
    alert_group_comments: list[dict],
    investigation_reports: list[dict],
    doc_context: str,
    examples: list[dict] | None = None,
) -> str:
    evidence_note = (
        "Используй investigation_reports как главный evidence layer."
        if investigation_reports
        else (
            "investigation_reports пуст: формируй выводы только по "
            "alert_group_comments и явно не заявляй подтвержденные root cause."
        )
    )
    return _build_prompt(
        role=(
            "Ты Final Summarizer, автор executive summary мониторинга "
            "Collection."
        ),
        goal=(
            "Сформировать компактное итоговое заключение для аналитика и "
            "руководителя."
        ),
        context=(
            "Не пересказывай все алерты подряд. Разделяй expected events и "
            f"potential incidents. {evidence_note}"
        ),
        doc_context=doc_context,
        input_data={
            "monitoring_stats": monitoring_stats,
            "alert_group_comments": alert_group_comments,
            "investigation_reports": investigation_reports,
        },
        output_rules=(
            "Приоритизируй наиболее важные инциденты и проверки. Не добавляй "
            "root cause, который не подтвержден investigation_reports."
        ),
        target_schema=FinalSummary.model_json_schema(),
        examples=examples,
    )


def build_repair_json_prompt(
    raw_response: str,
    validation_error: str,
    target_schema: dict,
) -> str:
    return (
        "# Роль\n"
        "Ты JSON Repairer.\n\n"
        "# Цель\n"
        "Исправить структуру невалидного ответа без изменения его смысла.\n\n"
        "# Контекст\n"
        "Не добавляй новые факты и не меняй бизнесовый смысл. Проведи "
        "внутреннюю проверку, но не показывай ход рассуждений.\n\n"
        "# Контекст документации\n"
        "Документация для repair не требуется.\n\n"
        "# Входные данные\n"
        f"{_json({'raw_response': raw_response, 'validation_error': validation_error})}\n\n"
        "# Выходные данные\n"
        "Верни только исправленный валидный JSON без markdown, объяснений и "
        "текста вокруг.\n\n"
        "# Выходная JSON schema\n"
        f"{_json(target_schema)}"
    )


# Compatibility aliases for the first GigaChat prototype.
def build_alert_group_prompt(alert_group: dict[str, Any]) -> str:
    return build_alert_commentator_prompt(alert_group, doc_context="")


def build_repair_prompt(raw_response: str, validation_error: str) -> str:
    return build_repair_json_prompt(
        raw_response,
        validation_error,
        AlertGroupComment.model_json_schema(),
    )

