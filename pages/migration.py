from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from ui import CARD_COLORS, apply_figure_style, chart_card, insight_banner, kpi_card, pill_filter, simple_bar, simple_line


net_flow = simple_line(
    [
        {"name": "США", "x": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023], "y": [0.42, 0.45, 0.48, 0.50, 0.53, 0.57, 0.58, 0.60], "color": "#149A98"},
        {"name": "Германия", "x": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023], "y": [0.08, 0.10, 0.13, 0.15, 0.18, 0.22, 0.25, 0.28], "color": "#E58400"},
        {"name": "Китай", "x": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023], "y": [-0.05, -0.08, -0.11, -0.13, -0.14, -0.15, -0.16, -0.17], "color": "#6D35FF"},
        {"name": "Индия", "x": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023], "y": [-0.10, -0.12, -0.14, -0.17, -0.19, -0.21, -0.22, -0.23], "color": "#FF3B30"},
    ],
)

receivers = simple_bar(
    ["США", "Германия", "Канада", "Австралия", "Великобритания", "Франция", "Испания"],
    [1.020, 0.680, 0.437, 0.395, 0.330, 0.275, 0.252],
    ["#149A98", "#149A98", "#149A98", "#2F63FF", "#2F63FF", "#2F63FF", "#2F63FF"],
    horizontal=True,
)

donors = simple_bar(
    ["Индия", "Китай", "Мексика", "Пакистан", "Филиппины", "Бангладеш", "Нигерия"],
    [0.680, 0.558, 0.445, 0.387, 0.312, 0.278, 0.245],
    ["#E32626"] * 7,
    horizontal=True,
)

skills = go.Figure()
skills.add_bar(name="Высокая", x=["США", "Германия", "Канада", "ОАЭ", "Австралия", "UK"], y=[45, 38, 52, 28, 48, 42], marker_color="#149A98")
skills.add_bar(name="Средняя", x=["США", "Германия", "Канада", "ОАЭ", "Австралия", "UK"], y=[31, 34, 27, 33, 29, 30], marker_color="#5F86E5")
skills.add_bar(name="Низкая", x=["США", "Германия", "Канада", "ОАЭ", "Австралия", "UK"], y=[24, 28, 21, 39, 23, 28], marker_color="#C2CAD8")
skills.update_layout(barmode="stack")
skills = apply_figure_style(skills)


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Миграционные потоки и структура рабочей силы", className="page-title"),
                html.P("Динамика чистой миграции · Страны-доноры/реципиенты · Квалификация мигрантов", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Группа стран",
                        dcc.Dropdown(
                            options=["ОЭСР", "Европа", "Азия", "Северная Америка", "Мир"],
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
                        dcc.Slider(
                            min=1990,
                            max=2023,
                            step=1,
                            value=2023,
                            marks={1990: "1990", 2000: "2000", 2010: "2010", 2023: "2023"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Тип миграции",
                        dbc.RadioItems(
                            options=[
                                {"label": "Чистая", "value": "net"},
                                {"label": "Приток", "value": "inflow"},
                                {"label": "Отток", "value": "outflow"},
                            ],
                            value="net",
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
                dbc.Col(kpi_card("Миг-ы в мире", "281M", "3,6% мирового населения", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Топ-реципиент · США", "+1.02M", "Чистый приток 2023", CARD_COLORS["blue"]), lg=3, md=6),
                dbc.Col(kpi_card("Топ-донор · Индия", "−0.68M", "Чистый отток 2023", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Высококвал. мигранты", "31.4%", "Среди всех мигрантов", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Тренд чистой миграции",
                        "Ежегодные чистые потоки 1990–2023 · Ключевые экономики (млн чел.)",
                        net_flow,
                        CARD_COLORS["blue"],
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
                        "Страны-реципиенты",
                        "Чистый приток 2023 (млн)",
                        receivers,
                        CARD_COLORS["teal"],
                        footer="Источник: Всемирный банк WDI · База ОЭСР по миграции",
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Страны-доноры",
                        "Чистый отток 2023 (млн)",
                        donors,
                        CARD_COLORS["red"],
                        footer="Отрицательные значения = больше эмигрантов, чем иммигрантов.",
                    ),
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Квалификация мигрантов",
                        "Распределение по квалификации и стране назначения",
                        skills,
                        CARD_COLORS["violet"],
                        footer="Источник: ОЭСР · Классификация ISCO-08",
                    ),
                    lg=4,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
        insight_banner(
            "Миграция частично компенсирует дефицит рабочей силы в стареющих экономиках ОЭСР, "
            "особенно при росте доли квалифицированных мигрантов."
        ),
    ],
    fluid=True,
)
