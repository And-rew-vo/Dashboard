"""Обзорная страница: ключевые KPI и сводные диаграммы по всему миру."""
from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import data as D
import insights as I
from ui import (CARD_COLORS, PALETTE, apply_layout, chart_card, fmt_num,
                fmt_pct, kpi_card, pill_filter)


def _world_kpis():
    df = D.load()
    wld = df[df["country_code"] == "WLD"]
    if wld.empty:
        return ("—", "—", "—", "—", "—", "—", "—", "—")
    pop = wld[wld["indicator"] == "SP.POP.TOTL"].sort_values("year").iloc[-1]
    p65 = wld[wld["indicator"] == "SP.POP.65UP.TO.ZS"].sort_values("year").iloc[-1]
    dpnd = wld[wld["indicator"] == "SP.POP.DPND"].sort_values("year").iloc[-1]
    le = wld[wld["indicator"] == "SP.DYN.LE00.IN"].sort_values("year").iloc[-1]
    return (
        fmt_num(pop["value"]), f"{int(pop['year'])} г., мир",
        fmt_pct(p65["value"]), f"{int(p65['year'])} г.",
        fmt_pct(dpnd["value"]), f"{int(dpnd['year'])} г.",
        f"{le['value']:.1f} лет", f"{int(le['year'])} г.",
    )


def _trend_age_structure() -> go.Figure:
    df = D.load()
    wld = df[df["country_code"] == "WLD"]
    fig = go.Figure()
    parts = [
        ("SP.POP.0014.TO.ZS", "0–14", PALETTE["cyan"]),
        ("SP.POP.1564.TO.ZS", "15–64", PALETTE["indigo"]),
        ("SP.POP.65UP.TO.ZS", "65+",   PALETTE["amber"]),
    ]
    for ind, name, color in parts:
        sub = wld[wld["indicator"] == ind].sort_values("year")
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines", name=name,
            line=dict(width=0.5, color=color), stackgroup="one",
            hovertemplate=f"{name}: %{{y:.1f}}%<extra>%{{x}}</extra>"))
    fig.update_yaxes(title=None, ticksuffix="%")
    return apply_layout(fig, height=340)


def _top_old_countries() -> go.Figure:
    df = D.by_indicator("SP.POP.65UP.TO.ZS")
    latest = df["year"].max()
    top = df[df["year"] == latest].nlargest(12, "value").sort_values("value")
    fig = go.Figure(go.Bar(
        x=top["value"], y=top["country"], orientation="h",
        marker=dict(color=top["value"], colorscale=[[0, PALETTE["emerald"]],
                                                    [1, PALETTE["rose"]]],
                    line=dict(width=0)),
        text=[f"{v:.1f}%" for v in top["value"]],
        textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    fig.update_xaxes(ticksuffix="%")
    return apply_layout(fig, height=340, legend=False,
                        margin=dict(l=8, r=40, t=10, b=10))


def _migration_world() -> go.Figure:
    df = D.load()
    df = df[(df["indicator"] == "SM.POP.NETM") & (~df["is_aggregate"])]
    # Aggregate by year — sum positive (receivers) vs negative (donors)
    df["sign"] = df["value"].apply(lambda v: "Реципиенты" if v > 0 else "Доноры")
    grouped = df.groupby(["year", "sign"])["value"].sum().reset_index()
    fig = go.Figure()
    for sign, color in [("Реципиенты", PALETTE["indigo"]),
                        ("Доноры", PALETTE["rose"])]:
        sub = grouped[grouped["sign"] == sign].sort_values("year")
        fig.add_trace(go.Bar(
            x=sub["year"], y=sub["value"]/1e6, name=sign,
            marker_color=color,
            hovertemplate=f"{sign}: %{{y:.2f}} млн<extra>%{{x}}</extra>"))
    fig.update_layout(barmode="relative")
    fig.update_yaxes(title="млн чел.", zeroline=True,
                     zerolinecolor="#cbd5e1", zerolinewidth=1)
    return apply_layout(fig, height=340)


k = _world_kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Старение населения и глобальная миграция", className="page-title"),
                html.P("Анализ влияния демографических сдвигов и миграционных потоков "
                       "на макроэкономическую устойчивость стран мира. "
                       "Данные: World Bank — Population Estimates, WDI, Net Migration.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Население мира", k[0], k[1],
                                 CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Доля 65+", k[2], k[3],
                                 CARD_COLORS["orange"]), lg=3, md=6),
                dbc.Col(kpi_card("Демогр. нагрузка", k[4], k[5],
                                 CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("Ожид. продолжит. жизни", k[6], k[7],
                                 CARD_COLORS["teal"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Динамика, мир",
                        "Возрастная структура населения мира",
                        CARD_COLORS["blue"],
                        _trend_age_structure(),
                        extra="доли 0–14 / 15–64 / 65+",
                    ),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Топ-12",
                        "Страны с самой высокой долей 65+",
                        CARD_COLORS["red"],
                        _top_old_countries(),
                        extra="последний год",
                    ),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Глобальная миграция",
                        "Суммарная чистая миграция: доноры vs реципиенты",
                        CARD_COLORS["teal"],
                        _migration_world(),
                        extra="млн чел. за 5-летний период",
                    ),
                    lg=12, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.overview_insights()),
    ],
    fluid=True,
)
