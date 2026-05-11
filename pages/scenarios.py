"""Сценарии и сравнение развитых vs развивающихся стран."""
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
    fert_hic = df[(df["country_code"] == "HIC") & (df["indicator"] == "SP.DYN.TFRT.IN")].sort_values("year").iloc[-1]
    fert_lic = df[(df["country_code"] == "LIC") & (df["indicator"] == "SP.DYN.TFRT.IN")].sort_values("year").iloc[-1]
    p65_hic = df[(df["country_code"] == "HIC") & (df["indicator"] == "SP.POP.65UP.TO.ZS")].sort_values("year").iloc[-1]
    p65_lic = df[(df["country_code"] == "LIC") & (df["indicator"] == "SP.POP.65UP.TO.ZS")].sort_values("year").iloc[-1]
    return (
        f"{fert_hic['value']:.2f}", "развитые страны",
        f"{fert_lic['value']:.2f}", "низкий доход",
        f"{p65_hic['value']:.1f}%", "65+ развитые",
        f"{p65_lic['value']:.1f}%", "65+ низкий доход",
    )


def _scenario_projection() -> go.Figure:
    """Условные сценарии доли 65+ к 2050: базовый, низкая миграция, высокая миграция.
    Базовая траектория — линейная экстраполяция тренда последних 20 лет."""
    df = D.load()
    fig = go.Figure()
    base_2050_targets = {}
    for code, name, color in [
        ("WLD", "Мир", PALETTE["indigo"]),
        ("EUU", "ЕС", PALETTE["rose"]),
        ("JPN", "Япония", PALETTE["amber"]),
    ]:
        sub = df[(df["country_code"] == code) &
                 (df["indicator"] == "SP.POP.65UP.TO.ZS")].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines", name=name,
            line=dict(width=2.6, color=color),
            hovertemplate=f"{name}: %{{y:.1f}}%<extra>%{{x}}</extra>"))
        # crude linear projection from last 20y
        recent = sub.tail(20)
        if len(recent) >= 5:
            x = recent["year"].values
            y = recent["value"].values
            slope = (y[-1] - y[0]) / (x[-1] - x[0])
            future_x = list(range(int(x[-1]) + 1, 2051))
            future_y = [y[-1] + slope * (fx - x[-1]) for fx in future_x]
            fig.add_trace(go.Scatter(
                x=future_x, y=future_y, mode="lines",
                name=f"{name} (прогноз)", line=dict(width=2, color=color, dash="dot"),
                showlegend=False,
                hovertemplate=f"{name} прогноз: %{{y:.1f}}%<extra>%{{x}}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    fig.add_vline(x=2024, line_dash="dash", line_color="#94a3b8", opacity=0.5)
    return apply_layout(fig, height=340)


def _dev_vs_dev() -> go.Figure:
    """Развитые vs развивающиеся: ключевые метрики, последний год."""
    df = D.load()
    metrics = [
        ("SP.POP.65UP.TO.ZS", "Доля 65+"),
        ("SP.DYN.LE00.IN", "Прод. жизни"),
        ("SP.DYN.TFRT.IN", "Рожд.×10"),
        ("NY.GDP.MKTP.KD.ZG", "Рост ВВП"),
        ("SH.XPD.CHEX.GD.ZS", "Здравоохр %"),
    ]
    groups = [("HIC", "Развитые", PALETTE["indigo"]),
              ("UMC", "Выше среднего", PALETTE["emerald"]),
              ("LMC", "Ниже среднего", PALETTE["amber"]),
              ("LIC", "Низкий доход", PALETTE["rose"])]
    fig = go.Figure()
    for code, name, color in groups:
        vals = []
        for ind, _ in metrics:
            sub = df[(df["country_code"] == code) & (df["indicator"] == ind)].sort_values("year")
            if sub.empty:
                vals.append(0)
            else:
                v = sub.iloc[-1]["value"]
                if ind == "SP.DYN.TFRT.IN":
                    v = v * 10
                vals.append(v)
        fig.add_trace(go.Bar(
            x=[m[1] for m in metrics], y=vals, name=name,
            marker_color=color,
            hovertemplate=f"{name} %{{x}}: %{{y:.1f}}<extra></extra>"))
    fig.update_layout(barmode="group")
    return apply_layout(fig, height=340)


def _investment_chart() -> go.Figure:
    """Инвестиции (% ВВП) по группам стран — долгосрочная устойчивость."""
    df = D.load()
    df = df[df["indicator"] == "NE.GDI.TOTL.ZS"]
    fig = go.Figure()
    for code in ["WLD", "HIC", "UMC", "LMC", "LIC"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.4),
            hovertemplate="%{y:.1f}%<extra>%{x}</extra>"))
    fig.update_yaxes(ticksuffix="%")
    return apply_layout(fig, height=340)


def _fertility_trends() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SP.DYN.TFRT.IN"]
    fig = go.Figure()
    for code in ["WLD", "HIC", "UMC", "LMC", "LIC", "SSF"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"], mode="lines",
            name=sub["country"].iloc[0], line=dict(width=2.4),
            hovertemplate="%{y:.2f}<extra>%{x}</extra>"))
    fig.add_hline(y=2.1, line_dash="dash", line_color="#94a3b8",
                  annotation_text="порог замещения (2.1)",
                  annotation_position="top right")
    return apply_layout(fig, height=340)


k = _kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Сценарии и сравнения", className="page-title"),
                html.P("Прогнозные траектории старения и контрастные демографические "
                       "профили развитых и развивающихся стран.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Рожд. (HIC)", k[0], k[1], CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Рожд. (LIC)", k[2], k[3], CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("65+ (HIC)", k[4], k[5], CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("65+ (LIC)", k[6], k[7], CARD_COLORS["orange"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Прогноз", "Доля 65+: история и линейная проекция до 2050",
                               CARD_COLORS["blue"], _scenario_projection(),
                               extra="пунктир — экстраполяция"),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Сравнение", "Развитые vs развивающиеся",
                               CARD_COLORS["teal"], _dev_vs_dev(),
                               extra="ключевые метрики"),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Рождаемость", "Коэффициент рождаемости по группам",
                               CARD_COLORS["violet"], _fertility_trends(),
                               extra="детей на женщину"),
                    lg=7, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Инвестиции", "Накопление капитала (% ВВП)",
                               CARD_COLORS["orange"], _investment_chart(),
                               extra="индикатор долгосрочной устойчивости"),
                    lg=5, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.scenarios_insights()),
    ],
    fluid=True,
)
