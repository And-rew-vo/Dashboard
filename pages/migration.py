from dash import dcc, html
import dash_bootstrap_components as dbc

from ui import CARD_COLORS, chart_card, kpi_card, pill_filter


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Миграция", className="page-title"),
                html.P("Страница для потоков, стран-доноров и реципиентов, а также структуры миграции.", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Группа объектов",
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
                        "Год",
                        dcc.Slider(
                            min=2000,
                            max=2025,
                            step=1,
                            value=2023,
                            marks={2000: "2000", 2010: "2010", 2020: "2020", 2025: "2025"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Тип потока",
                        dbc.RadioItems(
                            options=[
                                {"label": "Общий", "value": "all"},
                                {"label": "Приток", "value": "in"},
                                {"label": "Отток", "value": "out"},
                            ],
                            value="all",
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
                dbc.Col(kpi_card("Карточка миграции 1", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка миграции 2", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка миграции 3", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка миграции 4", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Широкий блок",
                        "Линейная диаграмма потоков",
                        CARD_COLORS["blue"],
                        extra="Во всю ширину",
                    ),
                    lg=12,
                    className="mb-4",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Левый блок",
                        "Рейтинг / диаграмма 1",
                        CARD_COLORS["teal"],
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Центральный блок",
                        "Рейтинг / диаграмма 2",
                        CARD_COLORS["red"],
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Правый блок",
                        "Составная диаграмма структуры",
                        CARD_COLORS["violet"],
                    ),
                    lg=4,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
    ],
    fluid=True,
)
