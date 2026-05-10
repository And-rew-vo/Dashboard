from dash import dcc, html
import dash_bootstrap_components as dbc

from ui import CARD_COLORS, chart_card, kpi_card, pill_filter


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Экономика", className="page-title"),
                html.P("Страница для экономических показателей, сравнений, расходов и долгосрочных сценариев.", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Экономический блок",
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
                            min=2000,
                            max=2050,
                            step=5,
                            value=[2005, 2035],
                            marks={2000: "2000", 2010: "2010", 2020: "2020", 2030: "2030", 2050: "2050"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Сценарий",
                        dbc.RadioItems(
                            options=[
                                {"label": "Базовый", "value": "base"},
                                {"label": "Сценарий 2", "value": "s2"},
                                {"label": "Сценарий 3", "value": "s3"},
                            ],
                            value="base",
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
                dbc.Col(kpi_card("Карточка экономики 1", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка экономики 2", CARD_COLORS["orange"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка экономики 3", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка экономики 4", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Левый верхний блок",
                        "Точечная / сравнительная диаграмма",
                        CARD_COLORS["red"],
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Правый верхний блок",
                        "Столбчатая / временная диаграмма",
                        CARD_COLORS["teal"],
                    ),
                    lg=7,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Левый нижний блок",
                        "Линейная диаграмма занятости",
                        CARD_COLORS["blue"],
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Центральный нижний блок",
                        "Группированная диаграмма расходов",
                        CARD_COLORS["orange"],
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Правый нижний блок",
                        "Диаграмма прогноза / сценария",
                        CARD_COLORS["violet"],
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
