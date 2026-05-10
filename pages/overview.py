from dash import dcc, html
import dash_bootstrap_components as dbc

from ui import CARD_COLORS, chart_card, kpi_card, pill_filter


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Обзор проекта", className="page-title"),
                html.P("Главная страница со сводными карточками, фильтрами и ключевыми диаграммами.", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Регион",
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
                            max=2025,
                            step=1,
                            value=[2010, 2023],
                            marks={2000: "2000", 2010: "2010", 2020: "2020", 2025: "2025"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Режим отображения",
                        dbc.RadioItems(
                            options=[
                                {"label": "Все объекты", "value": "all"},
                                {"label": "Группа 1", "value": "group_1"},
                                {"label": "Группа 2", "value": "group_2"},
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
                dbc.Col(kpi_card("Карточка показателя 1", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка показателя 2", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка показателя 3", CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("Карточка показателя 4", CARD_COLORS["red"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Блок диаграммы",
                        "Диаграмма 1",
                        CARD_COLORS["blue"],
                        extra="Левая колонка",
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Блок диаграммы",
                        "Диаграмма 2",
                        CARD_COLORS["red"],
                        extra="Центральная колонка",
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Блок диаграммы",
                        "Диаграмма 3",
                        CARD_COLORS["orange"],
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
