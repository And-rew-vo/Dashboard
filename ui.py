from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


APP_TITLE = "Дашборд"
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


def kpi_card(title: str, accent: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="metric-label"),
                html.Div("—", className="metric-value metric-placeholder"),
                html.Div("Место для значения показателя", className="metric-note"),
            ]
        ),
        className="metric-card",
        style={"--accent-color": accent},
    )


def empty_figure(label: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=label,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=18, color="#8FA1BA"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="#F4F8FF",
        margin=dict(l=20, r=20, t=18, b=20),
    )
    return fig


def chart_card(
    eyebrow: str,
    title: str,
    accent: str,
    extra: str | None = None,
    height_class: str = "",
    placeholder: str = "Область для диаграммы",
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

    classes = "chart-card"
    if height_class:
        classes = f"{classes} {height_class}"

    return dbc.Card(
        [
            header,
            dbc.CardBody(
                [
                    dcc.Graph(
                        figure=empty_figure(placeholder),
                        config={"displayModeBar": False},
                        className="chart-graph",
                    )
                ]
            ),
        ],
        className=classes,
        style={"--accent-color": accent},
    )


def note_card(title: str, text: str, accent: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="metric-label"),
                html.Div(text, className="mini-card-text"),
            ]
        ),
        className="mini-note-card",
        style={"--accent-color": accent},
    )


def pill_filter(label: str, control: html.Div) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="filter-label"),
            control,
        ],
        className="filter-pill",
    )
