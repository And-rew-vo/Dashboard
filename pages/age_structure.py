from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from ui import CARD_COLORS, chart_card, insight_banner, kpi_card, pill_filter, population_pyramid, simple_bar, simple_line


age_groups = ["85+", "80–84", "75–79", "70–74", "65–69", "60–64", "55–59", "50–54", "45–49", "40–44", "35–39", "30–34", "25–29", "20–24", "15–19", "10–14", "5–9", "0–4"]
male_2023 = [1.5, 2.1, 2.8, 4.0, 5.0, 5.5, 6.1, 6.3, 6.0, 5.6, 5.1, 4.6, 4.2, 4.5, 5.1, 5.6, 5.2, 4.8]
female_2023 = [2.6, 3.1, 3.8, 5.0, 5.8, 6.2, 6.9, 7.1, 6.8, 6.2, 5.8, 5.3, 4.9, 5.4, 5.8, 6.0, 5.7, 5.2]

pyramid = population_pyramid(male_2023, female_2023, age_groups)

aging_japan = simple_line(
    [
        {"name": "Япония", "x": [1960, 1970, 1980, 1990, 2000, 2010, 2023, 2030], "y": [5.7, 6.3, 7.5, 11.9, 17.4, 23.0, 29.1, 30.0], "color": "#FF3B30"},
    ],
    y_suffix="%",
)

regional_stack = go.Figure()
regions = ["Вост. Азия", "Зап. Ев.", "Сев. Ам.", "Лат. Ам.", "Юж. Азия", "Суб-Сах."]
regional_stack.add_bar(name="Пожилые 65+", x=regions, y=[15, 21, 17, 9, 6, 1], marker_color="#E32626")
regional_stack.add_bar(name="Трудосп. 15–64", x=regions, y=[66, 63, 65, 67, 69, 60], marker_color="#1F9A93")
regional_stack.add_bar(name="Молодёжь 0–14", x=regions, y=[19, 16, 18, 24, 25, 39], marker_color="#E58400")
regional_stack.update_layout(barmode="stack")
from ui import apply_figure_style
regional_stack = apply_figure_style(regional_stack)

dependency_economies = simple_line(
    [
        {"name": "Япония", "x": [1990, 2000, 2010, 2015, 2020, 2025, 2030], "y": [8, 12, 18, 23, 27, 33, 41], "color": "#E65454"},
        {"name": "Европа", "x": [1990, 2000, 2010, 2015, 2020, 2025, 2030], "y": [10, 12, 13, 15, 17, 18, 20], "color": "#E58400"},
        {"name": "Мир", "x": [1990, 2000, 2010, 2015, 2020, 2025, 2030], "y": [7, 8, 9, 9.5, 10, 11, 12], "color": "#149A98"},
        {"name": "Китай", "x": [1990, 2000, 2010, 2015, 2020, 2025, 2030], "y": [5, 7, 9, 11, 13, 17, 24], "color": "#3E72E7"},
    ],
)


layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Возрастная структура и демографическая нагрузка", className="page-title"),
                html.P("Половозрастные пирамиды · Доля трудоспособных · Доля пожилых по регионам · 2023", className="page-subtitle"),
            ],
            className="page-heading",
        ),
        dbc.Row(
            [
                dbc.Col(
                    pill_filter(
                        "Страна",
                        dcc.Dropdown(
                            options=["Япония", "Италия", "Германия", "Китай", "США"],
                            value="Япония",
                            clearable=False,
                        ),
                    ),
                    lg=3,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Период сравнения",
                        dcc.RangeSlider(
                            min=1960,
                            max=2030,
                            step=10,
                            value=[1990, 2023],
                            marks={1960: "1960", 1980: "1980", 2000: "2000", 2020: "2020", 2030: "2030"},
                        ),
                    ),
                    lg=5,
                    md=6,
                    className="mb-3",
                ),
                dbc.Col(
                    pill_filter(
                        "Показатель",
                        dbc.RadioItems(
                            options=[
                                {"label": "65+", "value": "65plus"},
                                {"label": "15–64", "value": "working"},
                                {"label": "0–14", "value": "young"},
                            ],
                            value="65plus",
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
                dbc.Col(kpi_card("Доля 65+ — Япония", "29.1%", "с 12,0% в 1990 г.", CARD_COLORS["red"]), lg=3, md=6),
                dbc.Col(kpi_card("Трудосп. воз. 15–64", "59.5%", "с 69,7% в 1995 г.", CARD_COLORS["teal"]), lg=3, md=6),
                dbc.Col(kpi_card("Молодёжь 0–14", "11.4%", "Минимум в мире", CARD_COLORS["orange"]), lg=3, md=6),
                dbc.Col(kpi_card("Коэф. нагрузки", "71.5", "На 100 трудоспособных", CARD_COLORS["violet"]), lg=3, md=6),
            ],
            className="g-3 mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    chart_card(
                        "Половозрастная пирамида",
                        "Япония 2023 vs 1990",
                        pyramid,
                        CARD_COLORS["teal"],
                        extra="призрак = данные 1990",
                        footer="Источник: Всемирный банк · ООН WPP 2022",
                    ),
                    lg=5,
                    className="mb-4",
                ),
                dbc.Col(
                    [
                        chart_card(
                            "Индекс старения",
                            "Доля 65+ — Япония 1960–2030",
                            aging_japan,
                            CARD_COLORS["red"],
                            extra="29.1% факт 2023",
                        ),
                        chart_card(
                            "Возрастная структура по регионам",
                            "Молодёжь · Трудосп. · Пожилые · 2023",
                            regional_stack,
                            CARD_COLORS["orange"],
                            height_class="mt-3",
                        ),
                    ],
                    lg=4,
                    className="mb-4",
                ),
                dbc.Col(
                    chart_card(
                        "Динамика коэф. нагрузки",
                        "Ключевые экономики 1990–2030",
                        dependency_economies,
                        CARD_COLORS["violet"],
                        extra="→ прогноз",
                        footer="Источник: Всемирный банк · ОЭСР · Пунктир = прогноз.",
                    ),
                    lg=3,
                    className="mb-4",
                ),
            ],
            className="g-3",
        ),
        insight_banner(
            "Коэффициент нагрузки выше 50 заметно сужает пространство для бюджетного манёвра и требует "
            "реформ пенсионных систем в стареющих экономиках."
        ),
    ],
    fluid=True,
)
