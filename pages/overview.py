from dash import dcc, html
import dash_bootstrap_components as dbc

from ui import CARD_COLORS, chart_card, insight_banner, kpi_card, pill_filter, simple_bar, simple_line


region_share = simple_bar(
    ["Зап. Европа", "Вост. Европа", "Сев. Ам.", "Вост. Азия", "Лат. Ам.", "Юж. Азия", "Суб-Сах."],
    [21, 18, 17, 15, 9, 6, 3],
    ["#E32626", "#E32626", "#E32626", "#E58400", "#E58400", "#1F9A93", "#1F9A93"],
)

aging_trend = simple_line(
    [
        {"name": "Мир", "x": [1990, 2000, 2010, 2020, 2030], "y": [6, 7.2, 8.6, 9.8, 11.5], "color": "#149A98"},
        {"name": "Европа", "x": [1990, 2000, 2010, 2020, 2030], "y": [13.2, 15.1, 18.0, 20.6, 23.4], "color": "#E58400"},
        {"name": "Япония", "x": [1990, 2000, 2010, 2020, 2030], "y": [12.0, 17.3, 22.8, 28.5, 31.2], "color": "#FF3B30"},
    ],
    y_suffix="%",
)

dependency_top = simple_bar(
    ["Япония", "Финляндия", "Италия", "Германия", "Франция", "Швеция", "США", "Индия", "Китай", "Нигерия"],
    [71.5, 68.2, 65.8, 63.4, 61.7, 60.5, 54.3, 47.2, 44.8, 86.4],
    ["#E32626", "#E32626", "#E58400", "#E58400", "#E58400", "#E58400", "#149A98", "#149A98", "#149A98", "#6D35FF"],
    horizontal=True,
)


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Глобальный демографический обзор", className="page-title"),
                html.P("Старение населения и миграция · Мировой срез · 2023", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Регион",
                        dcc.Dropdown(
                            options=["Мир", "Европа", "Азия", "Северная Америка", "Латинская Америка", "Африка"],
                            value="Мир",
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
                        "Срез",
                        dbc.RadioItems(
                            options=[
                                {"label": "Все страны", "value": "all"},
                                {"label": "Развитые", "value": "advanced"},
                                {"label": "Развивающиеся", "value": "emerging"},
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
                dbc.Col(kpi_card("Население 65+", "10.1%", "+1.3 пп с 2015 г.", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Коэф. нагрузки", "52.3", "+4.1 пт с 2000 г.", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Миг-ы в мире", "281M", "3,6% мирового населения", CARD_COLORS["violet"]), lg=3, md=6),
                dbc.Col(kpi_card("Корр. стар–ВВП", "−0.61", "Сильная отрицательная связь", CARD_COLORS["red"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Географическое распределение",
                        "Доля населения 65+ по регионам",
                        region_share,
                        CARD_COLORS["blue"],
                        extra="2023",
                        footer="Источник: Всемирный банк · ОЭСР · ООН",
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Тренд старения",
                        "Доля населения 65+",
                        aging_trend,
                        CARD_COLORS["red"],
                        extra="1990 – 2030",
                        footer="Данные: Всемирный банк. Прогноз: ООН WPP 2022.",
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    [
                        chart_card(
                            "Коэф. демографической нагрузки",
                            "Топ стран · 2023",
                            dependency_top,
                            CARD_COLORS["orange"],
                            extra="на 100 трудоспособных",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Ключевой вывод", className="metric-label"),
                                    html.Div(
                                        "К 2030 г. в Японии будет менее 1,25 работника на пенсионера.",
                                        className="mini-card-text",
                                    ),
                                ]
                            ),
                            className="mini-note-card mt-3",
                            style={"--accent-color": CARD_COLORS["teal"]},
                        ),
                    ],
                    lg=3,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
        insight_banner(
            "Каждый прирост коэф. нагрузки на 1 пп связан со снижением потенциального роста ВВП "
            "и участия в рынке труда в стареющих экономиках."
        ),
    ],
    fluid=True,
)
