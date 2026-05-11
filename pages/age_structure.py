"""Возрастная структура: пирамида, доли 65+, динамика по странам."""
from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import data as D
import insights as I
from ui import (CARD_COLORS, PALETTE, apply_layout, chart_card, fmt_num,
                fmt_pct, kpi_card, pill_filter)


HIGHLIGHT_COUNTRIES = ["JPN", "DEU", "ITA", "FRA", "USA", "CHN", "IND", "RUS",
                       "BRA", "NGA", "ZAF"]


def _kpis():
    df = D.load()
    p65 = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    latest = p65[p65["year"] == p65["year"].max()]
    top = latest.nlargest(1, "value").iloc[0]
    bot = latest[latest["value"] > 0].nsmallest(1, "value").iloc[0]

    dep = df[(df["indicator"] == "SP.POP.DPND.OL") & (df["country_code"] == "WLD")]
    dep_latest = dep.sort_values("year").iloc[-1]

    fert = df[(df["indicator"] == "SP.DYN.TFRT.IN") & (df["country_code"] == "WLD")]
    fert_latest = fert.sort_values("year").iloc[-1]

    return (
        f"{top['value']:.1f}%", f"{top['country']}, {int(top['year'])}",
        f"{bot['value']:.1f}%", f"{bot['country']}, {int(bot['year'])}",
        f"{dep_latest['value']:.1f}", f"мир, {int(dep_latest['year'])} г.",
        f"{fert_latest['value']:.2f}", f"мир, {int(fert_latest['year'])} г.",
    )


def _ratio_chart() -> go.Figure:
    df = D.load()
    fig = go.Figure()
    for i, code in enumerate(["JPN", "DEU", "ITA", "USA", "CHN", "IND", "WLD"]):
        sub = df[(df["country_code"] == code) &
                 (df["indicator"] == "SP.POP.65UP.TO.ZS")].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines", name=sub["country"].iloc[0],
            line=dict(width=2.6),
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


def _dependency_chart() -> go.Figure:
    df = D.load()
    fig = go.Figure()
    for ind, name, color in [
        ("SP.POP.DPND.YG", "Дети (0–14)", PALETTE["cyan"]),
        ("SP.POP.DPND.OL", "Пожилые (65+)", PALETTE["rose"]),
    ]:
        sub = df[(df["country_code"] == "WLD") & (df["indicator"] == ind)].sort_values("year")
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines", name=name,
            line=dict(width=2.6, color=color),
            fill="tonexty" if ind == "SP.POP.DPND.OL" else "tozeroy",
            fillcolor=("rgba(244,63,94,0.10)" if ind == "SP.POP.DPND.OL"
                       else "rgba(6,182,212,0.10)"),
            hovertemplate=f"{name}: %{{y:.1f}}<extra>%{{x}}</extra>"))
    return apply_layout(fig, height=340)


def _aging_speed_chart() -> go.Figure:
    df = D.by_indicator("SP.POP.65UP.TO.ZS")
    latest_year = int(df["year"].max())
    base_year = max(1990, latest_year - 25)
    pivot = df.pivot_table(index="country", columns="year", values="value")
    if base_year not in pivot.columns or latest_year not in pivot.columns:
        years = sorted([c for c in pivot.columns if isinstance(c, int)])
        base_year, latest_year = years[0], years[-1]
    delta = (pivot[latest_year] - pivot[base_year]).dropna()
    top = delta.nlargest(15).sort_values()
    fig = go.Figure(go.Bar(
        x=top.values, y=top.index, orientation="h",
        marker=dict(color=top.values,
                    colorscale=[[0, PALETTE["amber"]], [1, PALETTE["rose"]]]),
        text=[f"+{v:.1f} п.п." for v in top.values],
        textposition="outside",
        hovertemplate="%{y}: +%{x:.2f} п.п.<extra></extra>"))
    fig.update_xaxes(ticksuffix=" п.п.")
    return apply_layout(fig, height=340, legend=False,
                        margin=dict(l=8, r=70, t=10, b=10))


def _life_expectancy_chart() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SP.DYN.LE00.IN"]
    df = df[df["country_code"].isin(["WLD", "HIC", "UMC", "LMC", "LIC"])]
    fig = go.Figure()
    for code in ["WLD", "HIC", "UMC", "LMC", "LIC"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.6),
            hovertemplate="%{y:.1f} лет<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix=" лет")
    return apply_layout(fig, height=340)


k = _kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Возрастная структура", className="page-title"),
                html.P("Доли возрастных групп, коэффициенты демографической нагрузки и сравнение динамики старения по странам.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Самая «старая» страна", k[0], k[1], CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Самая «молодая» страна", k[2], k[3], CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Нагрузка пожилыми", k[4], k[5], CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("Коэф. рождаемости", k[6], k[7], CARD_COLORS["orange"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Динамика", "Доля 65+ по ключевым странам",
                               CARD_COLORS["blue"], _ratio_chart(),
                               extra="% от общего населения"),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Нагрузка", "Коэффициент демографической нагрузки (мир)",
                               CARD_COLORS["violet"], _dependency_chart(),
                               extra="на 100 трудоспособных"),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Скорость старения",
                               "Прирост доли 65+ за последние 25 лет",
                               CARD_COLORS["red"], _aging_speed_chart(),
                               extra="топ-15 стран"),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card("По группам доходов",
                               "Ожидаемая продолжительность жизни",
                               CARD_COLORS["teal"], _life_expectancy_chart(),
                               extra="мир и группы по доходу"),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.age_insights()),
    ],
    fluid=True,
)
