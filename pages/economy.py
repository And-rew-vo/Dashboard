"""Экономика: ВВП, занятость, расходы и связь со старением."""
from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import data as D
import insights as I
from ui import (CARD_COLORS, PALETTE, apply_layout, chart_card, fmt_num,
                fmt_pct, kpi_card, pill_filter)


def _kpis():
    df = D.load()
    wld = df[df["country_code"] == "WLD"]
    g = wld[wld["indicator"] == "NY.GDP.MKTP.KD.ZG"].sort_values("year").iloc[-1]
    gpc = wld[wld["indicator"] == "NY.GDP.PCAP.CD"].sort_values("year").iloc[-1]
    emp = wld[wld["indicator"] == "SL.EMP.TOTL.SP.ZS"].sort_values("year").iloc[-1]
    hx = wld[wld["indicator"] == "SH.XPD.CHEX.GD.ZS"].sort_values("year").iloc[-1]
    return (
        f"{g['value']:.1f}%", f"мир, {int(g['year'])} г.",
        fmt_num(gpc["value"], " $"), f"мир, {int(gpc['year'])} г.",
        f"{emp['value']:.1f}%", f"мир, {int(emp['year'])} г.",
        f"{hx['value']:.1f}%", f"% ВВП, {int(hx['year'])} г.",
    )


def _aging_gdp_scatter() -> go.Figure:
    """Связь: доля 65+ vs ВВП на душу (последний год)."""
    df = D.load()
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    gdp = df[(df["indicator"] == "NY.GDP.PCAP.CD") & (~df["is_aggregate"])]
    y_age = age["year"].max()
    y_gdp = gdp["year"].max()
    merged = age[age["year"] == y_age].merge(
        gdp[gdp["year"] == y_gdp], on="country_code", suffixes=("_age", "_gdp"))
    fig = go.Figure(go.Scatter(
        x=merged["value_age"], y=merged["value_gdp"], mode="markers+text",
        text=merged["country_age"], textposition="top center",
        textfont=dict(size=9, color="#475569"),
        marker=dict(size=10, color=merged["value_age"],
                    colorscale=[[0, PALETTE["cyan"]], [0.5, PALETTE["indigo"]],
                                [1, PALETTE["rose"]]],
                    line=dict(width=1, color="white"),
                    showscale=False),
        hovertemplate="<b>%{text}</b><br>65+: %{x:.1f}%<br>ВВП/чел: $%{y:,.0f}<extra></extra>"))
    fig.update_layout(yaxis_type="log")
    fig.update_xaxes(title="Доля 65+, %", ticksuffix="%")
    fig.update_yaxes(title="ВВП на душу, $ (log)")
    return apply_layout(fig, height=340, legend=False)


def _gdp_growth_chart() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "NY.GDP.MKTP.KD.ZG"]
    fig = go.Figure()
    for code in ["WLD", "HIC", "UMC", "LMC", "LIC"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.4),
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%", zeroline=True, zerolinecolor="#cbd5e1")
    return apply_layout(fig, height=340)


def _employment_chart() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SL.EMP.TOTL.SP.ZS"]
    fig = go.Figure()
    for code in ["JPN", "DEU", "USA", "RUS", "CHN", "IND", "BRA"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.2),
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


def _health_vs_aging_chart() -> go.Figure:
    """Расходы на здравоохранение vs доля 65+."""
    df = D.load()
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    hx = df[(df["indicator"] == "SH.XPD.CHEX.GD.ZS") & (~df["is_aggregate"])]
    y = min(age["year"].max(), hx["year"].max())
    a = age[age["year"] == y][["country_code", "country", "value"]]
    h = hx[hx["year"] == y][["country_code", "value"]]
    m = a.merge(h, on="country_code", suffixes=("_age", "_hx"))
    fig = go.Figure(go.Scatter(
        x=m["value_age"], y=m["value_hx"], mode="markers",
        marker=dict(size=10, color=m["value_age"],
                    colorscale=[[0, PALETTE["cyan"]], [1, PALETTE["rose"]]],
                    line=dict(width=1, color="white")),
        text=m["country"],
        hovertemplate="<b>%{text}</b><br>65+: %{x:.1f}%<br>Здравоохр: %{y:.1f}% ВВП<extra></extra>"))
    fig.update_xaxes(title="Доля 65+, %", ticksuffix="%")
    fig.update_yaxes(title="Расходы на здравоохр., % ВВП", ticksuffix="%")
    return apply_layout(fig, height=340, legend=False)


def _gov_spending_chart() -> go.Figure:
    """Государственные расходы vs старение (последний год)."""
    df = D.load()
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    gov = df[(df["indicator"] == "NE.CON.GOVT.ZS") & (~df["is_aggregate"])]
    y = min(age["year"].max(), gov["year"].max())
    m = age[age["year"] == y][["country_code", "country", "value"]].merge(
        gov[gov["year"] == y][["country_code", "value"]],
        on="country_code", suffixes=("_age", "_gov"))
    fig = go.Figure(go.Scatter(
        x=m["value_age"], y=m["value_gov"], mode="markers",
        marker=dict(size=11, color=m["value_age"],
                    colorscale=[[0, PALETTE["emerald"]], [1, PALETTE["violet"]]],
                    line=dict(width=1, color="white")),
        text=m["country"],
        hovertemplate="<b>%{text}</b><br>65+: %{x:.1f}%<br>Госрасходы: %{y:.1f}% ВВП<extra></extra>"))
    fig.update_xaxes(title="Доля 65+, %", ticksuffix="%")
    fig.update_yaxes(title="Госрасходы, % ВВП", ticksuffix="%")
    return apply_layout(fig, height=340, legend=False)


def _sectors_chart() -> go.Figure:
    """Структура ВВП по секторам, последний год, выбранные страны."""
    df = D.load()
    codes = ["JPN", "DEU", "USA", "RUS", "CHN", "IND", "BRA", "NGA"]
    sectors = [
        ("NV.AGR.TOTL.ZS", "С/х", PALETTE["emerald"]),
        ("NV.IND.MANF.ZS", "Промышл.", PALETTE["amber"]),
        ("NV.SRV.TOTL.ZS", "Услуги", PALETTE["indigo"]),
    ]
    rows = []
    for code in codes:
        for ind, _, _ in sectors:
            sub = df[(df["country_code"] == code) & (df["indicator"] == ind)].sort_values("year")
            if sub.empty:
                continue
            rows.append((sub["country"].iloc[0], ind, sub.iloc[-1]["value"]))
    if not rows:
        return apply_layout(go.Figure(), height=340)
    fig = go.Figure()
    countries = list(dict.fromkeys(r[0] for r in rows))
    for ind, name, color in sectors:
        vals = []
        for c in countries:
            v = next((r[2] for r in rows if r[0] == c and r[1] == ind), 0)
            vals.append(v)
        fig.add_trace(go.Bar(
            x=countries, y=vals, name=name, marker_color=color,
            hovertemplate=f"{name}: %{{y:.1f}}%<extra>%{{x}}</extra>"))
    fig.update_layout(barmode="stack")
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


def _unemployment_chart() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SL.UEM.TOTL.ZS"]
    fig = go.Figure()
    for code in ["WLD", "HIC", "UMC", "LMC", "LIC", "EUU"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.4),
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


def _income_groups_aging() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SP.POP.65UP.TO.ZS"]
    fig = go.Figure()
    for code in ["HIC", "UMC", "LMC", "LIC"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0],
            line=dict(width=2.6), stackgroup=None,
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


k = _kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Экономика", className="page-title"),
                html.P("Влияние демографических сдвигов на ВВП, занятость, "
                       "производительность и государственные расходы.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Рост ВВП", k[0], k[1], CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("ВВП на душу", k[2], k[3], CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Уровень занятости", k[4], k[5], CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("Расходы на здравоохр.", k[6], k[7], CARD_COLORS["red"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Связь", "Старение vs богатство страны",
                               CARD_COLORS["blue"], _aging_gdp_scatter(),
                               extra="последний год, log-шкала"),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Рост", "Динамика роста ВВП по группам стран",
                               CARD_COLORS["teal"], _gdp_growth_chart(),
                               extra="% в год"),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Занятость", "Уровень занятости по странам",
                               CARD_COLORS["violet"], _employment_chart(),
                               extra="% населения 15+"),
                    lg=6, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Безработица", "Уровень безработицы по группам стран",
                               CARD_COLORS["red"], _unemployment_chart(),
                               extra="% рабочей силы"),
                    lg=6, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Расходы", "Здравоохранение vs старение",
                               CARD_COLORS["pink"], _health_vs_aging_chart(),
                               extra="% ВВП"),
                    lg=4, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Госрасходы", "Госрасходы vs старение",
                               CARD_COLORS["orange"], _gov_spending_chart(),
                               extra="конечное потребление, % ВВП"),
                    lg=4, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Группы дохода", "Доля 65+ по группам",
                               CARD_COLORS["cyan"], _income_groups_aging(),
                               extra="HIC / UMC / LMC / LIC"),
                    lg=4, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Структура экономики",
                               "Состав ВВП по секторам, последний год",
                               CARD_COLORS["teal"], _sectors_chart(),
                               extra="с/х + промышленность + услуги"),
                    lg=12, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.economy_insights()),
    ],
    fluid=True,
)
