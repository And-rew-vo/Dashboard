from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from ui import CARD_COLORS, apply_figure_style, chart_card, insight_banner, kpi_card, pill_filter, simple_line, simple_scatter


scatter = simple_scatter(
    [
        {
            "name": "Страны",
            "x": [6.2, 5.8, 4.1, 3.2, 3.0, 2.6, 2.1, 1.9],
            "y": [0.8, 0.5, 1.7, 2.0, 2.2, 2.8, 3.1, 3.5],
            "labels": ["ЯП", "ИТ", "КТЙ", "ИНД", "БРА", "США", "ИНДО", "НИГ"],
            "sizes": [24, 22, 20, 18, 18, 26, 20, 20],
            "colors": ["#E32626", "#F07F7F", "#4C78E8", "#5F86E5", "#149A98", "#149A98", "#E58400", "#6D35FF"],
        }
    ]
)

gdp_growth = go.Figure()
years = list(range(2000, 2024))
values = [0.8, 1.0, 1.1, 1.3, 2.0, 1.8, 1.5, 2.1, 0.6, -1.0, 2.2, 1.3, 1.4, 0.8, 1.0, 0.9, 1.3, 1.4, 1.5, 1.6, -1.1, 1.5, 1.4, 1.0]
colors = ["#149A98" if value >= 0 else "#E94545" for value in values]
gdp_growth.add_bar(x=years, y=values, marker_color=colors)
gdp_growth = apply_figure_style(gdp_growth)

employment = simple_line(
    [
        {"name": "Стареющие эк.", "x": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2023], "y": [58, 58.5, 60, 58.5, 59, 60.5, 61.7, 59.2, 59.8], "color": "#E32626"},
        {"name": "Молодые экономики", "x": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2023], "y": [44, 46, 49.5, 50, 53, 56, 58.5, 60, 61.5], "color": "#149A98"},
        {"name": "Мир (ср.)", "x": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2023], "y": [52, 52.5, 53.5, 52.5, 53.5, 55.0, 56.0, 54.8, 55.9], "color": "#6B7C99"},
    ],
    y_suffix="%",
)

spending = go.Figure()
countries = ["Италия", "Франция", "Япония", "Германия", "США"]
spending.add_bar(name="Пенсии", y=countries, x=[16.2, 14.4, 11.2, 12.3, 7.1], orientation="h", marker_color="#E58400")
spending.add_bar(name="Здравоохранение", y=countries, x=[8.9, 11.1, 11.0, 11.7, 17.6], orientation="h", marker_color="#5F86E5")
spending.update_layout(barmode="group")
spending = apply_figure_style(spending)

debt = simple_line(
    [
        {"name": "Япония", "x": [2023, 2035, 2050], "y": [10.2, 10.5, 11.0], "color": "#E32626"},
        {"name": "США", "x": [2023, 2035, 2050], "y": [6.0, 6.3, 7.3], "color": "#149A98"},
        {"name": "ЕС", "x": [2023, 2035, 2050], "y": [5.2, 5.4, 6.2], "color": "#E58400"},
        {"name": "Китай", "x": [2023, 2035, 2050], "y": [5.0, 5.2, 6.0], "color": "#2F63FF"},
    ],
)


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Макроэкономическая устойчивость и влияние старения", className="page-title"),
                html.P("ВВП, занятость, пенсии/здравоохранение, долгосрочная динамика долга", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Экономический блок",
                        dcc.Dropdown(
                            options=["ВВП", "Занятость", "Расходы", "Долг"],
                            value="ВВП",
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
                            value=[2000, 2050],
                            marks={2000: "2000", 2010: "2010", 2020: "2020", 2035: "2035", 2050: "2050"},
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
                                {"label": "Высокая миграция", "value": "high_migration"},
                                {"label": "Низкая рождаемость", "value": "low_fertility"},
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
                dbc.Col(kpi_card("Рост ВВП — стареющие", "0.9%", "vs 2,8% в молодых экономиках", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Пенс. расходы (ЕС)", "13.2%", "% ВВП · ↑ с 9,1% в 2000 г.", CARD_COLORS["orange"]), lg=3, md=6),
                dbc.Col(kpi_card("Тренд расх. на здр.", "+0.4%", "ВВП/год на +5 лет ожид. жизни", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Разрыв производит.", "−18%", "Стареющие vs молодые экономики", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Корреляция старения и роста ВВП",
                        "Доля 65+ vs рост ВВП % · 2023",
                        scatter,
                        CARD_COLORS["red"],
                        extra="r = −0.61",
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Темп роста ВВП · мир (ср.)",
                        "Год. % · 2000–2023",
                        gdp_growth,
                        CARD_COLORS["teal"],
                        footer="Источник: Всемирный банк WDI · МВФ WEO 2023",
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
                        "Динамика занятости",
                        "Стареющие vs молодые экономики · 2000–2023",
                        employment,
                        CARD_COLORS["blue"],
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Госрасходы → % ВВП",
                        "Пенсии и здравоохранение · Отд. страны",
                        spending,
                        CARD_COLORS["orange"],
                        footer="Источник: ОЭСР · Eurostat",
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Прогноз госдолга / ВВП",
                        "Долгосрочный фискальный путь 2023–2050",
                        debt,
                        CARD_COLORS["violet"],
                        footer="Источник: МВФ · Всемирный банк",
                    ),
                    lg=3,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
        insight_banner(
            "Без миграции и реформ стареющие экономики упираются в структурное замедление роста: "
            "растут расходы, снижается участие в занятости и усиливается давление на долг."
        ),
    ],
    fluid=True,
)
