from dash import dcc, html
import dash_bootstrap_components as dbc

from ui import CARD_COLORS, chart_card, kpi_card, pill_filter


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Возрастная структура", className="page-title"),
                html.P("Страница для половозрастных диаграмм, структуры групп и сравнений по периодам.", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Объект сравнения",
                        dcc.Dropdown(
                            options=["Вариант 1", "Вариант 2", "Вариант 3"],
                            value="Вариант 1",
                            clearable=False,
                        ),
                    ),
                    lg=3,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Период",
                        dcc.RangeSlider(
                            min=1990,
                            max=2030,
                            step=5,
                            value=[2000, 2023],
                            marks={1990: "1990", 2000: "2000", 2010: "2010", 2020: "2020", 2030: "2030"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Категория",
                        dbc.RadioItems(
                            options=[
                                {"label": "Группа 1", "value": "g1"},
                                {"label": "Группа 2", "value": "g2"},
                                {"label": "Группа 3", "value": "g3"},
                            ],
                            value="g1",
                            inline=True,
                        ),
                    ),
                    lg=4,
                    md=12,
                    className="mb-3",
                ),
            ],
            className="g-3 mb-1",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Карточка структуры 1", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка структуры 2", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка структуры 3", CARD_COLORS["orange"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка структуры 4", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Основной блок",
                        "Половозрастная диаграмма",
                        CARD_COLORS["teal"],
                        extra="Крупный график",
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    [
                        chart_card(
                            "Средний блок",
                            "Диаграмма динамики",
                            CARD_COLORS["red"],
                            height_class="split-chart-card",
                        ),
                        chart_card(
                            "Средний блок",
                            "Составная диаграмма",
                            CARD_COLORS["orange"],
                            height_class="mt-3 split-chart-card",
                        ),
                    ],
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Боковой блок",
                        "Сравнение объектов",
                        CARD_COLORS["violet"],
                        extra="Правая колонка",
                    ),
                    lg=3,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
    ],
    fluid=True,
)
