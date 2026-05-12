from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


APP_TITLE = "Демография и макроэкономика"
TOPBAR_BUTTON = "Студенты: Волов, Тарнов, Черевко"

HEADER_TABS = [
    {"id": "nav-overview", "label": "Обзор", "href": "/overview"},
    {"id": "nav-age", "label": "Возрастная структура", "href": "/age-structure"},
    {"id": "nav-migration", "label": "Миграция", "href": "/migration"},
    {"id": "nav-economy", "label": "Экономика", "href": "/economy"},
    {"id": "nav-map", "label": "Карта мира", "href": "/map"},
    {"id": "nav-scenarios", "label": "Сценарии", "href": "/scenarios"},
]

PALETTE = {
    "indigo": "#5B6CFF",
    "emerald": "#10B981",
    "amber": "#F59E0B",
    "pink": "#EC4899",
    "cyan": "#06B6D4",
    "violet": "#8B5CF6",
    "rose": "#F43F5E",
    "slate": "#475569",
}

CARD_COLORS = {
    "blue": PALETTE["indigo"],
    "teal": PALETTE["emerald"],
    "violet": PALETTE["violet"],
    "red": PALETTE["rose"],
    "orange": PALETTE["amber"],
    "cyan": PALETTE["cyan"],
    "pink": PALETTE["pink"],
}

CHART_SEQUENCE = [
    PALETTE["indigo"], PALETTE["emerald"], PALETTE["amber"],
    PALETTE["pink"], PALETTE["cyan"], PALETTE["violet"],
    PALETTE["rose"], PALETTE["slate"],
]


CHART_H = 320  # стандартная высота диаграммы в ряду


def apply_layout(fig: go.Figure, *, height: int = CHART_H,
                 legend: bool = True, margin: dict | None = None) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=margin or dict(l=10, r=14, t=18, b=10),
        font=dict(family="Inter, Segoe UI, sans-serif", size=12,
                  color="#1d2740"),
        colorway=CHART_SEQUENCE,
        legend=dict(orientation="h", yanchor="bottom", y=-0.22,
                    xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)") if legend else dict(),
        showlegend=legend,
        hoverlabel=dict(bgcolor="white", font_family="Inter",
                        bordercolor="#d7e2f1"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#d7e2f1",
                     ticks="outside", tickcolor="#cfd8e8")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(143,161,186,0.18)",
                     zeroline=False, linecolor="rgba(0,0,0,0)")
    return fig


def kpi_card(title: str, value: str, note: str, accent: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="metric-label"),
                html.Div(value, className="metric-value"),
                html.Div(note, className="metric-note"),
            ]
        ),
        className="metric-card",
        style={"--accent-color": accent},
    )


def chart_card(eyebrow: str, title: str, accent: str, figure: go.Figure,
               extra: str | None = None, height_class: str = "",
               graph_id: str | None = None) -> dbc.Card:
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
    graph_kwargs = dict(figure=figure, config={"displayModeBar": False},
                        className="chart-graph")
    if graph_id:
        graph_kwargs["id"] = graph_id
    classes = "chart-card"
    if height_class:
        classes = f"{classes} {height_class}"
    return dbc.Card(
        [header, dbc.CardBody([dcc.Graph(**graph_kwargs)])],
        className=classes,
        style={"--accent-color": accent},
    )


def pill_filter(label: str, control) -> html.Div:
    return html.Div(
        [html.Div(label, className="filter-label"), control],
        className="filter-pill",
    )


def fmt_num(v, suffix: str = "", digits: int = 1) -> str:
    if v is None:
        return "—"
    av = abs(v)
    if av >= 1e9:
        return f"{v/1e9:.{digits}f} млрд{suffix}"
    if av >= 1e6:
        return f"{v/1e6:.{digits}f} млн{suffix}"
    if av >= 1e3:
        return f"{v/1e3:.{digits}f} тыс{suffix}"
    return f"{v:.{digits}f}{suffix}"


def fmt_pct(v) -> str:
    return "—" if v is None else f"{v:.1f}%"
