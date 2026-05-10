from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


APP_TITLE = "Демографик Пульс"
TOPBAR_BUTTON = "Экспорт отчёта"

HEADER_TABS = [
    {"id": "nav-overview", "label": "Обзор", "href": "/overview"},
    {"id": "nav-age", "label": "Возрастная структура", "href": "/age-structure"},
    {"id": "nav-migration", "label": "Миграция", "href": "/migration"},
    {"id": "nav-economy", "label": "Экономика", "href": "/economy"},
]

CARD_COLORS = {
    "blue": "#2F63FF",
    "teal": "#16B0A8",
    "violet": "#6D35FF",
    "red": "#FF3B30",
    "orange": "#E58400",
}

CHART_BG = "#F4F8FF"
GRID = "#DDE7F5"
TEXT_MUTED = "#8FA1BA"


def kpi_card(title: str, value: str, note: str, accent: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="metric-label"),
                html.Div(value, className="metric-value"),
                html.Div(note, className="metric-note", style={"color": accent}),
            ]
        ),
        className="metric-card",
        style={"--accent-color": accent},
    )


def chart_card(
    eyebrow: str,
    title: str,
    figure: go.Figure,
    accent: str,
    extra: str | None = None,
    footer: str | None = None,
    height_class: str = "",
) -> dbc.Card:
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(eyebrow, className="card-eyebrow"),
                    html.H3(title, className="chart-title"),
                ]
            ),
            html.Div(extra or "", className="card-extra"),
        ],
        className="chart-card-header",
    )
    body_children = [dcc.Graph(figure=figure, config={"displayModeBar": False}, className="chart-graph")]
    if footer:
        body_children.append(html.Div(footer, className="chart-footer"))

    classes = "chart-card"
    if height_class:
        classes = f"{classes} {height_class}"

    return dbc.Card(
        [header, dbc.CardBody(body_children)],
        className=classes,
        style={"--accent-color": accent},
    )


def insight_banner(text: str) -> html.Div:
    return html.Div(
        [
            html.Span("Ключевой вывод:", className="insight-title"),
            html.Span(text, className="insight-text"),
        ],
        className="insight-banner",
    )


def pill_filter(label: str, control: html.Div) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="filter-label"),
            control,
        ],
        className="filter-pill",
    )


def apply_figure_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor=CHART_BG,
        margin=dict(l=20, r=20, t=18, b=20),
        font=dict(family="Inter, Segoe UI, sans-serif", color="#1E2A44"),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=TEXT_MUTED)),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=TEXT_MUTED)),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, x=0),
    )
    return fig


def simple_bar(labels: list[str], values: list[float], colors: list[str], horizontal: bool = False) -> go.Figure:
    fig = go.Figure()
    if horizontal:
        fig.add_bar(
            y=labels,
            x=values,
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{value:g}" for value in values],
            textposition="outside",
        )
    else:
        fig.add_bar(
            x=labels,
            y=values,
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{value:g}%" for value in values],
            textposition="outside",
        )
    return apply_figure_style(fig)


def simple_line(series: list[dict], y_suffix: str = "") -> go.Figure:
    fig = go.Figure()
    for item in series:
        fig.add_trace(
            go.Scatter(
                x=item["x"],
                y=item["y"],
                mode="lines+markers",
                name=item["name"],
                line=dict(color=item["color"], width=3),
                marker=dict(size=7),
            )
        )
    fig = apply_figure_style(fig)
    if y_suffix:
        fig.update_yaxes(ticksuffix=y_suffix)
    return fig


def simple_scatter(points: list[dict]) -> go.Figure:
    fig = go.Figure()
    for item in points:
        fig.add_trace(
            go.Scatter(
                x=item["x"],
                y=item["y"],
                mode="markers+text",
                text=item["labels"],
                textposition="top center",
                marker=dict(size=item["sizes"], color=item["colors"], opacity=0.88, line=dict(width=0)),
                name=item["name"],
            )
        )
    fig = apply_figure_style(fig)
    return fig


def population_pyramid(male: list[int], female: list[int], groups: list[str]) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(
        y=groups,
        x=[-value for value in male],
        name="Мужчины 2023",
        orientation="h",
        marker_color="#1F9A93",
    )
    fig.add_bar(
        y=groups,
        x=female,
        name="Женщины 2023",
        orientation="h",
        marker_color="#E65454",
    )
    fig.update_layout(barmode="relative")
    fig = apply_figure_style(fig)
    fig.update_xaxes(tickvals=[-10, -5, 0, 5, 10], ticktext=["10", "5", "0", "5", "10"])
    return fig
