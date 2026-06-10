from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import pandas as pd


EXPECTED_CLASSIFICATIONS = {
    "expected_event",
    "expected_process_feature",
}
INCIDENT_CLASSIFICATIONS = {
    "potential_incident",
    "needs_manual_review",
}


def _escape(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _list_html(items: list[Any] | None) -> str:
    if not items:
        return '<p class="muted">No data</p>'
    return "<ul>" + "".join(f"<li>{_escape(item)}</li>" for item in items) + "</ul>"


def _badge(value: str, prefix: str = "") -> str:
    css_value = value.replace("_", "-")
    label = f"{prefix}{value}" if prefix else value
    return f'<span class="badge {css_value}">{_escape(label)}</span>'


def _alert_summary(alert: dict[str, Any]) -> str:
    return (
        f"<strong>{_escape(alert.get('metric'))}</strong> "
        f"({_escape(alert.get('severity'))}): "
        f"{_escape(alert.get('python_description'))}"
    )


def _related_alerts_html(alerts: list[dict[str, Any]]) -> str:
    if not alerts:
        return '<p class="muted">No related alerts</p>'
    rows = "".join(
        "<tr>"
        f"<td>{_escape(alert.get('metric'))}</td>"
        f"<td>{_escape(alert.get('severity'))}</td>"
        f"<td>{_escape(alert.get('current_value'))}</td>"
        f"<td>{_escape(alert.get('delta_abs'))}</td>"
        f"<td>{_escape(alert.get('python_description'))}</td>"
        "</tr>"
        for alert in alerts
    )
    return (
        "<table><thead><tr><th>Metric</th><th>Severity</th>"
        "<th>Current</th><th>Delta</th><th>Description</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _rag_sources_html(context: dict[str, Any] | None) -> str:
    chunks = (context or {}).get("chunks", [])
    if not chunks:
        return '<p class="muted">RAG context was not found.</p>'
    return "".join(
        '<div class="source">'
        f"<strong>{_escape(chunk.get('source'))}</strong> "
        f'<span class="score">score={_escape(chunk.get("score"))}</span>'
        f"<p>{_escape(chunk.get('text_preview'))}</p>"
        "</div>"
        for chunk in chunks
    )


def _charts_html(chart_paths: list[str]) -> str:
    if not chart_paths:
        return '<p class="muted">Charts are unavailable.</p>'
    return '<div class="charts">' + "".join(
        (
            '<figure><img loading="lazy" '
            f'src="charts/{_escape(path)}" alt="{_escape(path)}">'
            f"<figcaption>{_escape(path)}</figcaption></figure>"
        )
        for path in chart_paths
    ) + "</div>"


def _tool_results_html(tool_results: list[dict[str, Any]]) -> str:
    if not tool_results:
        return '<p class="muted">Diagnostic tools were not executed.</p>'
    rows = "".join(
        "<tr>"
        f"<td>{_escape(result.get('tool_name'))}</td>"
        f"<td>{_badge(str(result.get('status', 'unknown')))}</td>"
        f"<td>{_escape(result.get('finding'))}</td>"
        f"<td>{_escape(result.get('supports_hypothesis'))}</td>"
        "</tr>"
        for result in tool_results
    )
    return (
        "<table><thead><tr><th>Tool</th><th>Status</th>"
        "<th>Finding</th><th>Supports hypothesis</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _investigation_html(investigation: dict[str, Any] | None) -> str:
    if not investigation:
        return (
            '<section class="investigation">'
            "<h4>Investigation results</h4>"
            '<p class="muted">Investigation report is unavailable.</p>'
            "</section>"
        )

    tool_plan = investigation.get("tool_plan", {})
    selected_tools = tool_plan.get("selected_tools", [])
    report = investigation.get("investigation_report", {})
    selected_tools_html = _list_html(
        [
            (
                f"{tool.get('tool_name')}: {tool.get('reason')} "
                f"(expected: {tool.get('expected_evidence')})"
            )
            for tool in selected_tools
        ]
    )
    return (
        '<section class="investigation">'
        "<h4>Investigation results</h4>"
        '<div class="investigation-grid">'
        "<div><h5>Selected tools</h5>"
        f"{selected_tools_html}</div>"
        "<div><h5>Evidence summary</h5>"
        f"{_list_html(report.get('evidence_summary'))}</div>"
        "</div>"
        "<h5>Tool results</h5>"
        f"{_tool_results_html(investigation.get('tool_results', []))}"
        '<div class="root-cause">'
        "<h5>Root cause hypothesis</h5>"
        f"<p>{_escape(report.get('root_cause_hypothesis'))}</p>"
        '<div class="badges">'
        f"{_badge(str(report.get('confidence', 'unknown')), 'confidence: ')}"
        f"{_badge(str(report.get('needs_manual_review', False)), 'manual review: ')}"
        "</div></div>"
        "<h5>Recommended actions</h5>"
        f"{_list_html(report.get('recommended_actions'))}"
        "</section>"
    )


def _final_summary_html(
    final_summary: dict[str, Any] | None,
    fallback_summary: str,
) -> str:
    if not final_summary:
        return (
            "<h2>Executive summary</h2>"
            f'<section class="summary"><p>{_escape(fallback_summary)}</p>'
            '<p class="muted">Final LLM summary is unavailable.</p></section>'
        )
    return (
        "<h2>Executive summary</h2>"
        '<section class="summary">'
        '<div class="summary-heading">'
        f"<h3>Overall status: {_escape(final_summary.get('overall_status'))}</h3>"
        f"{_badge(str(final_summary.get('overall_status', 'unknown')))}"
        "</div>"
        f"<p>{_escape(final_summary.get('executive_summary'))}</p>"
        "<h4>Manager summary</h4>"
        f"<p>{_escape(final_summary.get('manager_summary'))}</p>"
        '<div class="summary-grid">'
        "<div><h4>Expected events</h4>"
        f"{_list_html(final_summary.get('expected_events'))}</div>"
        "<div><h4>Potential incidents</h4>"
        f"{_list_html(final_summary.get('potential_incidents'))}</div>"
        "<div><h4>Root cause hypotheses</h4>"
        f"{_list_html(final_summary.get('root_cause_hypotheses'))}</div>"
        "<div><h4>Priority checks</h4>"
        f"{_list_html(final_summary.get('priority_checks'))}</div>"
        "</div></section>"
    )


def _group_card(
    alert_group: dict[str, Any],
    comment: dict[str, Any],
    context: dict[str, Any] | None,
    investigation: dict[str, Any] | None,
    chart_paths: list[str],
) -> str:
    classification = str(
        comment.get("event_classification", "needs_manual_review")
    )
    return (
        f'<article class="alert-card" id="{_escape(alert_group["alert_group_id"])}">'
        '<div class="card-header">'
        f"<div><h3>{_escape(comment.get('short_title') or alert_group['event_type'])}</h3>"
        f'<p class="group-id">{_escape(alert_group["alert_group_id"])}</p></div>'
        '<div class="badges">'
        f"{_badge(classification)}"
        f"{_badge(str(comment.get('risk_level', 'unknown')), 'risk: ')}"
        f"{_badge(str(comment.get('confidence', 'unknown')), 'confidence: ')}"
        "</div></div>"
        '<div class="meta-grid">'
        f"<div><span>Event type</span>{_escape(alert_group.get('event_type'))}</div>"
        f"<div><span>Process</span>{_escape(alert_group.get('process'))}</div>"
        f"<div><span>Product</span>{_escape(alert_group.get('product'))}</div>"
        f"<div><span>Segment</span>{_escape(alert_group.get('segment'))}</div>"
        "</div>"
        f"<p class=\"conclusion\">{_escape(comment.get('short_conclusion'))}</p>"
        "<h4>Main alert</h4>"
        f"<p>{_alert_summary(alert_group['main_alert'])}</p>"
        "<h4>Related alerts</h4>"
        f"{_related_alerts_html(alert_group.get('related_alerts', []))}"
        "<h4>Charts</h4>"
        f"{_charts_html(chart_paths)}"
        '<div class="comment-grid">'
        f"<section><h4>Facts</h4>{_list_html(comment.get('facts'))}</section>"
        "<section><h4>Business interpretation</h4>"
        f"<p>{_escape(comment.get('business_interpretation'))}</p></section>"
        f"<section><h4>Possible causes</h4>{_list_html(comment.get('possible_causes'))}</section>"
        f"<section><h4>Recommended checks</h4>{_list_html(comment.get('recommended_checks'))}</section>"
        "</div>"
        "<h4>Retrieved RAG sources</h4>"
        f"{_rag_sources_html(context)}"
        f"{_investigation_html(investigation)}"
        "</article>"
    )


def build_human_report(
    monitoring_df: pd.DataFrame,
    alert_objects: list[dict],
    alert_groups: list[dict],
    alert_group_comments: list[dict],
    retrieved_contexts: list[dict],
    investigations: list[dict] | None,
    final_summary: dict[str, Any] | None,
    charts_by_group: dict[str, list[str]],
    output_path: Path,
) -> None:
    comments_by_id = {
        comment["alert_group_id"]: comment
        for comment in alert_group_comments
    }
    contexts_by_id = {
        context["alert_group_id"]: context
        for context in retrieved_contexts
    }
    investigations_by_id = {
        investigation["alert_group_id"]: investigation
        for investigation in (investigations or [])
    }

    expected_groups: list[dict] = []
    incident_groups: list[dict] = []
    group_cards: list[str] = []
    for alert_group in alert_groups:
        group_id = alert_group["alert_group_id"]
        comment = comments_by_id.get(
            group_id,
            {
                "alert_group_id": group_id,
                "short_title": alert_group["event_type"],
                "short_conclusion": "LLM comment is unavailable.",
                "event_classification": "needs_manual_review",
                "risk_level": "unknown",
                "confidence": "unknown",
            },
        )
        classification = comment["event_classification"]
        if classification in EXPECTED_CLASSIFICATIONS:
            expected_groups.append(alert_group)
        if classification in INCIDENT_CLASSIFICATIONS:
            incident_groups.append(alert_group)
        group_cards.append(
            _group_card(
                alert_group,
                comment,
                contexts_by_id.get(group_id),
                investigations_by_id.get(group_id),
                charts_by_group.get(group_id, []),
            )
        )

    critical_groups = sum(
        group.get("critical_count", 0) > 0 for group in alert_groups
    )
    technical_summary = (
        f"Monitoring contains {len(monitoring_df)} aggregated rows, "
        f"{len(alert_objects)} alert objects and {len(alert_groups)} alert "
        f"groups. {len(expected_groups)} groups are classified as expected "
        f"events or process features; {len(incident_groups)} groups require "
        "incident review."
    )

    nav_expected = _list_html(
        [
            f"{group['event_type']} — {group['alert_group_id']}"
            for group in expected_groups
        ]
    )
    nav_incidents = _list_html(
        [
            f"{group['event_type']} — {group['alert_group_id']}"
            for group in incident_groups
        ]
    )
    statistics = [
        ("Monitoring rows", len(monitoring_df)),
        ("Alert objects", len(alert_objects)),
        ("Alert groups", len(alert_groups)),
        ("Critical groups", critical_groups),
        ("Expected events", len(expected_groups)),
        ("Potential incidents", len(incident_groups)),
    ]
    statistics_html = "".join(
        f'<div class="stat"><strong>{value}</strong><span>{_escape(label)}</span></div>'
        for label, value in statistics
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Collection Monitoring Report</title>
  <style>
    :root {{
      --ink: #172033; --muted: #667085; --line: #dfe3ea;
      --panel: #ffffff; --canvas: #f4f6f9; --accent: #2458a6;
      --danger: #b42318; --warning: #b54708; --ok: #027a48;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); background: var(--canvas);
      font: 15px/1.55 Arial, sans-serif; }}
    main {{ max-width: 1320px; margin: 0 auto; padding: 36px 24px 80px; }}
    h1 {{ margin-bottom: 6px; font-size: 34px; }}
    h2 {{ margin-top: 42px; border-bottom: 2px solid var(--line);
      padding-bottom: 8px; }}
    h3 {{ margin: 0; font-size: 23px; }}
    h4 {{ margin: 24px 0 8px; }}
    .subtitle, .muted, .group-id {{ color: var(--muted); }}
    .summary, .alert-card, .index-panel {{ background: var(--panel);
      border: 1px solid var(--line); border-radius: 14px;
      box-shadow: 0 4px 16px rgba(23,32,51,.05); }}
    .summary {{ padding: 22px; }}
    .stats {{ display: grid; grid-template-columns: repeat(6, 1fr);
      gap: 12px; margin: 18px 0; }}
    .stat {{ padding: 18px; background: var(--panel); border: 1px solid var(--line);
      border-radius: 12px; text-align: center; }}
    .stat strong {{ display: block; font-size: 28px; color: var(--accent); }}
    .stat span {{ color: var(--muted); }}
    .index-grid, .comment-grid, .summary-grid, .investigation-grid {{
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 18px; }}
    .index-panel {{ padding: 18px 22px; }}
    .alert-card {{ padding: 24px; margin: 22px 0; }}
    .card-header {{ display: flex; justify-content: space-between; gap: 20px; }}
    .group-id {{ margin: 5px 0 0; font-family: monospace; font-size: 12px; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 7px; align-content: start; }}
    .badge {{ display: inline-block; border-radius: 999px; padding: 5px 10px;
      background: #eef2f7; font-size: 12px; font-weight: bold; }}
    .expected-event, .expected-process-feature, .low {{ color: var(--ok);
      background: #ecfdf3; }}
    .potential-incident, .high {{ color: var(--danger); background: #fef3f2; }}
    .needs-manual-review, .medium {{ color: var(--warning); background: #fffaeb; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr);
      gap: 10px; margin: 18px 0; }}
    .meta-grid div {{ background: #f8fafc; padding: 10px; border-radius: 8px; }}
    .meta-grid span {{ display: block; color: var(--muted); font-size: 12px; }}
    .conclusion {{ font-size: 17px; border-left: 4px solid var(--accent);
      padding: 10px 14px; background: #f7faff; }}
    .summary-heading {{ display: flex; justify-content: space-between;
      align-items: center; gap: 15px; }}
    .summary-grid > div, .investigation-grid > div {{
      background: #f8fafc; border-radius: 10px; padding: 4px 14px; }}
    .investigation {{ margin-top: 24px; border-top: 2px solid var(--line);
      padding-top: 4px; }}
    .root-cause {{ border-left: 4px solid var(--warning);
      background: #fffcf5; padding: 4px 14px 14px; margin-top: 16px; }}
    h5 {{ margin: 16px 0 6px; font-size: 14px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border: 1px solid var(--line); padding: 8px; text-align: left; }}
    th {{ background: #f8fafc; }}
    .charts {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px; }}
    figure {{ margin: 0; border: 1px solid var(--line); border-radius: 10px;
      overflow: hidden; background: white; }}
    figure img {{ display: block; width: 100%; height: auto; }}
    figcaption {{ padding: 7px 10px; color: var(--muted); font-size: 11px; }}
    .source {{ border-left: 3px solid #98a2b3; padding: 8px 12px;
      margin: 10px 0; background: #f8fafc; }}
    .source p {{ margin-bottom: 0; }}
    .score {{ color: var(--muted); font-size: 12px; }}
    @media (max-width: 900px) {{
      .stats, .meta-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .index-grid, .comment-grid, .summary-grid, .investigation-grid,
      .charts {{ grid-template-columns: 1fr; }}
      .card-header {{ display: block; }}
    }}
  </style>
</head>
<body>
<main>
  <h1>Collection Monitoring Report</h1>
  <p class="subtitle">Demo run technical report</p>

  {_final_summary_html(final_summary, technical_summary)}

  <h2>Monitoring statistics</h2>
  <section class="stats">{statistics_html}</section>

  <div class="index-grid">
    <section class="index-panel">
      <h2>Expected events</h2>{nav_expected}
    </section>
    <section class="index-panel">
      <h2>Potential incidents</h2>{nav_incidents}
    </section>
  </div>

  <h2>Alert groups</h2>
  {''.join(group_cards)}
</main>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
