from __future__ import annotations

import json
from typing import Any

from src.schemas import (
    AlertGroupComment,
    FinalSummary,
    InvestigationToolPlan,
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


def _language_policy_section() -> str:
    return (
        "# Language policy\n"
        "Все человекочитаемые текстовые поля верни строго на русском языке.\n"
        "Не используй английские предложения.\n"
        "Не используй транслитерацию.\n"
        "Технические названия метрик, функций, JSON-полей и event_type можно "
        "оставлять как есть.\n"
        "Примеры допустимых технических терминов: target_rate, psi_score, "
        "reject_share, check_psi_shift, model_gini_drop.\n"
        "Ответ должен быть валидным JSON."
    )


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
        f"{_language_policy_section()}\n\n"
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
            "possible_causes являются только проверяемыми гипотезами. Если "
            "event_classification равен expected_event или "
            "expected_process_feature, не называй событие инцидентом в "
            "short_title, short_conclusion и business_interpretation. "
            "Используй формулировки «ожидаемое событие» или «ожидаемая "
            "особенность процесса». Для model_gini_drop поле threshold_abs "
            "является порогом величины падения Gini, а не минимально "
            "допустимым значением Gini. Сравнивай abs(delta_abs) с "
            "threshold_abs. Например, при current_value=0.31, "
            "previous_value=0.4261 и threshold_abs=0.07 пиши: «Снижение Gini "
            "составило 0.1161 и превысило порог значимого падения 0.07». "
            "Никогда не пиши, что значение Gini 0.31 ниже порога 0.07."
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
            "верни пустой selected_tools и объясни stop_reason. Ориентиры: "
            "для bank_unavailable_day сначала проверь календарь и объем; для "
            "credit_card_batch_inflow — календарь, продуктовый микс и при "
            "необходимости target rate; для model_gini_drop — target rate, "
            "PSI и распределение score; для empty_feature_vector — missing "
            "rate, пустые vectors и score distribution; для "
            "new_high_risk_segment — score distribution, target rate, PSI и "
            "product mix; для optimizer_mass_reject — reject share, "
            "communication mix и volume. Считай эти наборы рекомендуемым "
            "baseline: включай перечисленные tools, если они доступны в "
            "whitelist. Для bank_unavailable_day baseline обязательно "
            "включает check_known_event_calendar и check_volume_shift. Для "
            "optimizer_mass_reject baseline включает "
            "check_optimizer_reject_share, check_communication_mix_shift и "
            "check_volume_shift. Отклоняйся от baseline только если tool "
            "недоступен или явно нерелевантен, и укажи причину в stop_reason. "
            "Для expected_event выбирай не более двух tools. Для "
            "expected_process_feature выбирай не более трех tools: calendar, "
            "основную проверку особенности процесса и при необходимости одну "
            "связанную метрику. Не выбирай check_known_event_calendar для "
            "potential_incident. Не добавляй tools сверх baseline только для "
            "заполнения лимита."
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
        target_schema=InvestigationToolPlan.model_json_schema(),
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
            "needs_manual_review=true и снизь confidence. Учитывай "
            "event_classification из alert_comment. Для expected_event и "
            "expected_process_feature критический статус отдельной метрики "
            "может быть механическим результатом порога и не означает "
            "инцидент, если ожидаемое событие подтверждено."
        ),
        doc_context=doc_context,
        input_data={
            "alert_group": alert_group,
            "alert_comment": alert_comment,
            "tool_results": tool_results,
        },
        output_rules=(
            "evidence_summary должен перечислять только наблюдения из "
            "tool_results. root_cause_hypothesis должна оставаться гипотезой. "
            "Для expected_event и expected_process_feature не используй "
            "формулировки «потенциальная проблема», «инцидент», «сбой» или "
            "«ошибка» как трактовку события. recommended_actions должны быть "
            "контрольными: проверить завершение ожидаемого процесса и "
            "восстановление метрик, без аварийной эскалации. Для "
            "credit_card_batch_inflow объясни скачок объема и доли "
            "credit_card ожидаемым пакетным поступлением портфеля; рекомендуй "
            "контроль завершения загрузки и анализ метрик с учетом "
            "продуктового микса. Для bank_unavailable_day явно укажи, что "
            "критичное отклонение объема объяснено подтвержденным ЕДН и не "
            "является инцидентом. Для model_gini_drop threshold_abs означает "
            "порог величины падения: сравнивай abs(delta_abs) с "
            "threshold_abs и не утверждай, что текущее значение Gini ниже "
            "самого threshold_abs."
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
            "potential incidents. Общий статус critical не отменяет и не "
            "скрывает ожидаемые события. Ожидаемые события не эскалируй как "
            "инциденты и не описывай их в manager_summary как проблему, сбой "
            f"или ошибку. {evidence_note}"
        ),
        doc_context=doc_context,
        input_data={
            "monitoring_stats": monitoring_stats,
            "alert_group_comments": alert_group_comments,
            "investigation_reports": investigation_reports,
        },
        output_rules=(
            "Приоритизируй наиболее важные инциденты и проверки. "
            "expected_events должен перечислить все группы из "
            "alert_group_comments с классификацией expected_event или "
            "expected_process_feature. В expected_events верни только точные "
            "alert_group_id этих групп, по одному идентификатору на элемент. "
            "potential_incidents должен перечислить все группы с "
            "классификацией potential_incident или needs_manual_review. В "
            "potential_incidents также верни только точные alert_group_id, по "
            "одному идентификатору на элемент. Не пропускай ни одной группы и "
            "не помещай одну группу в оба списка. root_cause_hypotheses бери "
            "только из investigation_reports групп с классификацией "
            "potential_incident или needs_manual_review; объяснения "
            "expected_event и expected_process_feature не включай в список "
            "первопричин инцидентов. Не добавляй гипотезу, которая отсутствует "
            "в investigation_reports. Объединяй дублирующиеся priority checks "
            "и сохраняй итог компактным."
        ),
        target_schema=FinalSummary.model_json_schema(),
        examples=examples,
    )


def build_final_summary_consistency_repair_prompt(
    final_summary: dict,
    alert_group_comments: list[dict],
    consistency_errors: list[str],
    target_schema: dict,
) -> str:
    return (
        "# Роль\n"
        "Ты редактор итогового резюме мониторинга Collection.\n\n"
        "# Цель\n"
        "Исправить только состав expected_events и potential_incidents, чтобы "
        "они полностью соответствовали классификациям комментариев.\n\n"
        "# Контекст\n"
        "Сохрани overall_status, executive_summary, manager_summary, "
        "root_cause_hypotheses и priority_checks без изменения. "
        "expected_events должен содержать точные alert_group_id всех "
        "комментариев с event_classification expected_event или "
        "expected_process_feature. potential_incidents должен содержать "
        "точные alert_group_id всех комментариев с event_classification "
        "potential_incident или needs_manual_review. Не помещай ожидаемые "
        "события в potential_incidents. Не добавляй отсутствующие во входных "
        "данных группы.\n\n"
        "# Контекст документации\n"
        "Дополнительная документация не требуется.\n\n"
        f"{_language_policy_section()}\n\n"
        "# Входные данные\n"
        f"{_json({'final_summary': final_summary, 'alert_group_comments': alert_group_comments, 'consistency_errors': consistency_errors})}\n\n"
        "# Выходные данные\n"
        "Верни полный исправленный FinalSummary. В expected_events и "
        "potential_incidents используй только alert_group_id. Верни строго "
        "один JSON-объект без markdown и текста вокруг.\n\n"
        "# Выходная JSON schema\n"
        f"{_json(target_schema)}"
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
        f"{_language_policy_section()}\n\n"
        "# Входные данные\n"
        f"{_json({'raw_response': raw_response, 'validation_error': validation_error})}\n\n"
        "# Выходные данные\n"
        "Верни только исправленный валидный JSON без markdown, объяснений и "
        "текста вокруг.\n\n"
        "# Выходная JSON schema\n"
        f"{_json(target_schema)}"
    )


def build_translate_json_to_russian_prompt(
    validated_json: dict,
    target_schema: dict,
) -> str:
    return (
        "# Роль\n"
        "Ты редактор русскоязычных структурированных отчетов.\n\n"
        "# Цель\n"
        "Переписать человекочитаемые текстовые значения на русском языке, "
        "полностью сохранив смысл и JSON-структуру.\n\n"
        "# Контекст\n"
        "Не добавляй и не удаляй факты. Не меняй числа, boolean-значения, "
        "массивы, JSON-ключи, enum, идентификаторы и технические названия. "
        "Переводи только предложения и пояснения для человека.\n\n"
        "# Контекст документации\n"
        "Дополнительная документация не требуется.\n\n"
        f"{_language_policy_section()}\n\n"
        "# Входные данные\n"
        f"{_json(validated_json)}\n\n"
        "# Выходные данные\n"
        "Верни тот же JSON-объект. Перепиши английские человекочитаемые "
        "значения на естественный русский язык. Технические идентификаторы "
        "оставь без изменений. Не добавляй текст вокруг JSON.\n\n"
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
