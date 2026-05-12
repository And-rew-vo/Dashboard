"""Карта мира: интерактивное представление демографии и миграции."""
from __future__ import annotations

from dash import Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import data as D
import insights as I
from ui import (CARD_COLORS, PALETTE, apply_layout, chart_card, fmt_num,
                kpi_card, pill_filter)


MAP_OPTIONS = [
    {"label": "Доля 65+ (% населения)", "value": "SP.POP.65UP.TO.ZS"},
    {"label": "Доля 15–64 (% населения)", "value": "SP.POP.1564.TO.ZS"},
    {"label": "Демогр. нагрузка", "value": "SP.POP.DPND"},
    {"label": "Чистая миграция (чел.)", "value": "SM.POP.NETM"},
    {"label": "ВВП на душу ($)", "value": "NY.GDP.PCAP.CD"},
    {"label": "Ожид. продолжит. жизни", "value": "SP.DYN.LE00.IN"},
    {"label": "Коэф. рождаемости", "value": "SP.DYN.TFRT.IN"},
    {"label": "Расходы на здравоохр. (% ВВП)", "value": "SH.XPD.CHEX.GD.ZS"},
]


def _build_map(indicator: str, year: int) -> go.Figure:
    df = D.load()
    sub = df[(df["indicator"] == indicator) & (~df["is_aggregate"]) &
             (df["year"] == year)]
    if sub.empty:
        latest = df[(df["indicator"] == indicator) & (~df["is_aggregate"])]["year"].max()
        sub = df[(df["indicator"] == indicator) & (~df["is_aggregate"]) &
                 (df["year"] == latest)]
        year = int(latest)

    # diverging color scale for migration, sequential for others
    if indicator == "SM.POP.NETM":
        colorscale = [[0, PALETTE["rose"]], [0.5, "#f1f5f9"], [1, PALETTE["indigo"]]]
        zmid = 0
        values = sub["value"]
    else:
        colorscale = [[0, PALETTE["cyan"]], [0.5, PALETTE["indigo"]],
                      [1, PALETTE["rose"]]]
        zmid = None
        values = sub["value"]

    fig = go.Figure(go.Choropleth(
        locations=sub["country_code"], z=values, locationmode="ISO-3",
        text=sub["country"], colorscale=colorscale, zmid=zmid,
        marker_line_color="rgba(255,255,255,0.6)", marker_line_width=0.4,
        colorbar=dict(thickness=10, len=0.72, x=1.01, tickfont=dict(size=10),
                      outlinewidth=0),
        hovertemplate="<b>%{text}</b><br>%{z:,.2f}<extra></extra>",
    ))
    fig.update_geos(
        showcoastlines=False, showframe=False, showland=True,
        landcolor="#eef2f9", showocean=True, oceancolor="rgba(91,108,255,0.04)",
        projection_type="natural earth", bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=520, margin=dict(l=0, r=0, t=10, b=0),
        font=dict(family="Inter, Segoe UI, sans-serif", color="#1d2740"),
    )
    return fig


_DEFAULT_IND = "SP.POP.65UP.TO.ZS"
_DEFAULT_YEAR = int(D.by_indicator(_DEFAULT_IND)["year"].max())
_YEAR_RANGE = D.load()
_MIN_YEAR = int(_YEAR_RANGE["year"].min())
_MAX_YEAR = int(_YEAR_RANGE["year"].max())


def _summary_kpis():
    df = D.load()
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    yr = age["year"].max()
    latest = age[age["year"] == yr]
    return (
        f"{latest['value'].median():.1f}%", f"медиана, {int(yr)}",
        f"{latest['value'].max():.1f}%", f"{latest.nlargest(1,'value').iloc[0]['country']}",
        f"{latest['value'].min():.1f}%", f"{latest.nsmallest(1,'value').iloc[0]['country']}",
        f"{int((latest['value'] > 14).sum())}", "стран с долей 65+ > 14%",
    )


k = _summary_kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Карта мира", className="page-title"),
                html.P("Интерактивная карта: выберите индикатор и год - оценивайте "
                       "географическое распределение демографии и экономики.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter("Индикатор",
                                dcc.Dropdown(id="map-indicator",
                                             options=MAP_OPTIONS,
                                             value=_DEFAULT_IND,
                                             clearable=False)),
                    lg=5, md=12, className="mb-3",
                ),
                dbc.Col(
                    pill_filter("Год",
                                dcc.Slider(id="map-year",
                                           min=_MIN_YEAR, max=_MAX_YEAR, step=1,
                                           value=_DEFAULT_YEAR,
                                           marks={y: str(y) for y in
                                                  range(_MIN_YEAR, _MAX_YEAR + 1, 5)},
                                           tooltip={"placement": "bottom"})),
                    lg=7, md=12, className="mb-3",
                ),
            ],
            className="g-3 mb-1",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Медиана 65+", k[0], k[1], CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Максимум 65+", k[2], k[3], CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Минимум 65+", k[4], k[5], CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("«Старых» стран", k[6], k[7], CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("География", "Распределение индикатора по странам",
                               CARD_COLORS["blue"],
                               _build_map(_DEFAULT_IND, _DEFAULT_YEAR),
                               extra="наведите курсор на страну",
                               graph_id="world-map-graph"),
                    lg=12, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.map_insights()),
    ],
    fluid=True,
)


@callback(
    Output("world-map-graph", "figure"),
    Input("map-indicator", "value"),
    Input("map-year", "value"),
)
def _update_map(indicator, year):
    return _build_map(indicator, int(year))
