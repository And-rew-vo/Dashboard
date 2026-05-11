"""Миграция: чистые потоки, страны-доноры и реципиенты."""
from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import data as D
import insights as I
from ui import (CARD_COLORS, PALETTE, apply_layout, chart_card, fmt_num,
                fmt_pct, kpi_card, pill_filter)


def _kpis():
    df = D.by_indicator("SM.POP.NETM")
    latest = df[df["year"] == df["year"].max()]
    receivers = latest[latest["value"] > 0]["value"].sum()
    donors = latest[latest["value"] < 0]["value"].sum()
    top_recv = latest.nlargest(1, "value").iloc[0]
    top_donr = latest.nsmallest(1, "value").iloc[0]
    return (
        fmt_num(receivers, " чел."), f"приток, {int(latest['year'].iloc[0])} г.",
        fmt_num(abs(donors), " чел."), f"отток, {int(latest['year'].iloc[0])} г.",
        fmt_num(top_recv["value"], " чел."), f"{top_recv['country']}",
        fmt_num(abs(top_donr["value"]), " чел."), f"{top_donr['country']}",
    )


def _flows_line() -> go.Figure:
    df = D.load()
    df = df[df["indicator"] == "SM.POP.NETM"]
    fig = go.Figure()
    for code in ["USA", "DEU", "GBR", "RUS", "IND", "MEX", "SAU"]:
        sub = df[df["country_code"] == code].sort_values("year")
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["value"]/1e3, mode="lines+markers",
            name=sub["country"].iloc[0], line=dict(width=2.2),
            marker=dict(size=5),
            hovertemplate=f"{sub['country'].iloc[0]}: %{{y:.0f}} тыс<extra>%{{x}}</extra>"))
    fig.update_yaxes(title="тыс. чел.", zeroline=True, zerolinecolor="#cbd5e1")
    return apply_layout(fig, height=340)


def _top_receivers() -> go.Figure:
    df = D.by_indicator("SM.POP.NETM")
    latest = df[df["year"] == df["year"].max()]
    top = latest.nlargest(12, "value").sort_values("value")
    fig = go.Figure(go.Bar(
        x=top["value"]/1e3, y=top["country"], orientation="h",
        marker=dict(color=top["value"]/1e3,
                    colorscale=[[0, PALETTE["cyan"]], [1, PALETTE["indigo"]]]),
        text=[f"{v/1e3:.0f}" for v in top["value"]],
        textposition="outside",
        hovertemplate="%{y}: %{x:.0f} тыс<extra></extra>"))
    fig.update_xaxes(title="тыс. чел.")
    return apply_layout(fig, height=340, legend=False,
                        margin=dict(l=8, r=40, t=10, b=10))


def _top_donors() -> go.Figure:
    df = D.by_indicator("SM.POP.NETM")
    latest = df[df["year"] == df["year"].max()]
    top = latest.nsmallest(12, "value").sort_values("value", ascending=False)
    fig = go.Figure(go.Bar(
        x=top["value"]/1e3, y=top["country"], orientation="h",
        marker=dict(color=top["value"]/1e3,
                    colorscale=[[0, PALETTE["rose"]], [1, PALETTE["amber"]]]),
        text=[f"{v/1e3:.0f}" for v in top["value"]],
        textposition="outside",
        hovertemplate="%{y}: %{x:.0f} тыс<extra></extra>"))
    fig.update_xaxes(title="тыс. чел.")
    return apply_layout(fig, height=340, legend=False,
                        margin=dict(l=8, r=40, t=10, b=10))


def _compensation_chart() -> go.Figure:
    """Миграция как компенсация снижения трудоспособного населения."""
    df = D.load()
    fig = go.Figure()
    for ind, name, color, axis in [
        ("SP.POP.1564.TO.ZS", "Доля 15–64, %", PALETTE["indigo"], "y1"),
        ("SM.POP.NETM", "Чистая миграция, млн", PALETTE["emerald"], "y2"),
    ]:
        sub = df[(df["country_code"] == "EUU") & (df["indicator"] == ind)].sort_values("year")
        if sub.empty:
            continue
        y = sub["value"]/1e6 if ind == "SM.POP.NETM" else sub["value"]
        fig.add_trace(go.Scatter(
            x=sub["year"], y=y, mode="lines", name=name,
            line=dict(width=2.6, color=color), yaxis=axis,
            hovertemplate=f"{name}: %{{y:.2f}}<extra>%{{x}}</extra>"))
    fig.update_layout(
        yaxis=dict(title="Доля 15–64, %", ticksuffix="%"),
        yaxis2=dict(title="Чистая миграция, млн", overlaying="y", side="right",
                    showgrid=False),
    )
    return apply_layout(fig, height=340)


k = _kpis()


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Миграция", className="page-title"),
                html.P("Чистая миграция по странам, основные доноры и реципиенты, "
                       "роль миграции в компенсации снижения трудоспособного населения.",
                       className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Глобальный приток", k[0], k[1], CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Глобальный отток", k[2], k[3], CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Топ-реципиент", k[4], k[5], CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Топ-донор", k[6], k[7], CARD_COLORS["orange"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Динамика", "Чистая миграция: ключевые страны",
                               CARD_COLORS["blue"], _flows_line(),
                               extra="тыс. чел. за 5-летний период"),
                    lg=12, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Топ-12", "Страны-реципиенты",
                               CARD_COLORS["teal"], _top_receivers(),
                               extra="последний год"),
                    lg=6, className="mb-4",
                ),
                dbc.Col(
                    chart_card("Топ-12", "Страны-доноры",
                               CARD_COLORS["red"], _top_donors(),
                               extra="последний год"),
                    lg=6, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card("Компенсация", "ЕС: миграция vs трудоспособное население",
                               CARD_COLORS["violet"], _compensation_chart(),
                               extra="две оси Y"),
                    lg=12, className="mb-4",
                ),
            ],
            className="g-3",
        ),
        I.insights_section(I.migration_insights()),
    ],
    fluid=True,
)
