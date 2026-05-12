"""Автоматически собираемые выводы и рекомендации на основе датасетов."""
from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

import data as D


def _last(df, code, ind):
    s = df[(df["country_code"] == code) & (df["indicator"] == ind)].sort_values("year")
    if s.empty:
        return None, None
    r = s.iloc[-1]
    return float(r["value"]), int(r["year"])


def _first_and_last(df, code, ind, since=1990):
    s = df[(df["country_code"] == code) & (df["indicator"] == ind) &
           (df["year"] >= since)].sort_values("year")
    if len(s) < 2:
        return None
    return s.iloc[0], s.iloc[-1]


def overview_insights() -> list[dict]:
    df = D.load()
    out = []

    pair = _first_and_last(df, "WLD", "SP.POP.65UP.TO.ZS")
    if pair is not None:
        a, b = pair
        delta = b["value"] - a["value"]
        out.append({
            "title": "Старение ускоряется",
            "text": f"Доля 65+ в мире выросла с {a['value']:.1f}% в {int(a['year'])} "
                    f"до {b['value']:.1f}% в {int(b['year'])} (+{delta:.1f} п.п.).",
            "tone": "amber",
        })

    pair = _first_and_last(df, "WLD", "SP.POP.1564.TO.ZS")
    if pair is not None:
        a, b = pair
        diff = b["value"] - a["value"]
        sign = "выросла" if diff > 0 else "снизилась"
        out.append({
            "title": "Трудоспособное население",
            "text": f"Доля 15–64 в мире {sign} с {a['value']:.1f}% до {b['value']:.1f}% "
                    f"({diff:+.1f} п.п.). Это создаёт давление на пенсионные системы.",
            "tone": "indigo",
        })

    # top recipient/donor
    migr = D.by_indicator("SM.POP.NETM")
    latest = migr[migr["year"] == migr["year"].max()]
    if not latest.empty:
        top = latest.nlargest(1, "value").iloc[0]
        bot = latest.nsmallest(1, "value").iloc[0]
        out.append({
            "title": "Полюсы миграции",
            "text": f"Крупнейший реципиент - {top['country']} (+{top['value']/1e6:.1f} млн "
                    f"за 5 лет), крупнейший донор - {bot['country']} ({bot['value']/1e6:.1f} млн).",
            "tone": "emerald",
        })

    le = _last(df, "WLD", "SP.DYN.LE00.IN")
    if le[0] is not None:
        out.append({
            "title": "Ожидаемая продолжительность жизни",
            "text": f"В мире - {le[0]:.1f} лет ({le[1]}). Чем выше LE, тем больше "
                    f"нагрузка на здравоохранение и пенсионные системы.",
            "tone": "pink",
        })

    return out


def age_insights() -> list[dict]:
    df = D.load()
    out = []

    # who aged fastest
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    yr_max = int(age["year"].max())
    yr_min = max(1990, yr_max - 25)
    piv = age.pivot_table(index="country", columns="year", values="value")
    if yr_min in piv.columns and yr_max in piv.columns:
        delta = (piv[yr_max] - piv[yr_min]).dropna()
        leader = delta.idxmax()
        out.append({
            "title": "Лидеры старения",
            "text": f"Быстрее всех за {yr_max - yr_min} лет постарела {leader} "
                    f"(+{delta.max():.1f} п.п.). Следом: " +
                    ", ".join(delta.nlargest(4).index[1:].tolist()) + ".",
            "tone": "rose",
        })

    # old-age dependency
    pair = _first_and_last(df, "WLD", "SP.POP.DPND.OL")
    if pair is not None:
        a, b = pair
        out.append({
            "title": "Нагрузка пожилыми",
            "text": f"С {int(a['year'])} по {int(b['year'])} коэффициент вырос "
                    f"с {a['value']:.1f} до {b['value']:.1f} пожилых на 100 трудоспособных "
                    f"({(b['value']-a['value'])/a['value']*100:+.0f}%).",
            "tone": "amber",
        })

    # fertility below replacement
    fert = df[df["indicator"] == "SP.DYN.TFRT.IN"]
    latest = fert[fert["year"] == fert["year"].max()]
    below = latest[(latest["value"] < 2.1) & (~latest["country_code"].isin(D.AGGREGATE_CODES))]
    out.append({
        "title": "Ниже порога замещения",
        "text": f"{len(below)} стран из выборки имеют рождаемость ниже 2.1 - "
                f"уровня простого воспроизводства. Без миграции их население сократится.",
        "tone": "indigo",
    })

    # life expectancy gap
    hic = _last(df, "HIC", "SP.DYN.LE00.IN")
    lic = _last(df, "LIC", "SP.DYN.LE00.IN")
    if hic[0] and lic[0]:
        out.append({
            "title": "Разрыв в продолжительности жизни",
            "text": f"Разница между развитыми и беднейшими странами - {hic[0] - lic[0]:.1f} лет "
                    f"({hic[0]:.1f} vs {lic[0]:.1f}).",
            "tone": "emerald",
        })

    return out


def migration_insights() -> list[dict]:
    df = D.load()
    out = []
    migr = D.by_indicator("SM.POP.NETM")
    yr = migr["year"].max()
    latest = migr[migr["year"] == yr]

    receivers = latest[latest["value"] > 0]["value"].sum()
    donors = latest[latest["value"] < 0]["value"].sum()
    out.append({
        "title": "Глобальные потоки",
        "text": f"За {int(yr)} (5-летний период): чистый приток в страны-реципиенты "
                f"составил {receivers/1e6:.1f} млн, отток из стран-доноров "
                f"{abs(donors)/1e6:.1f} млн.",
        "tone": "indigo",
    })

    # top 3 each
    top_r = latest.nlargest(3, "value")
    top_d = latest.nsmallest(3, "value")
    out.append({
        "title": "Главные реципиенты",
        "text": "Крупнейшие принимающие страны: " +
                ", ".join([f"{r['country']} ({r['value']/1e6:+.2f} млн)"
                           for _, r in top_r.iterrows()]) + ".",
        "tone": "emerald",
    })
    out.append({
        "title": "Главные доноры",
        "text": "Крупнейшие отдающие страны: " +
                ", ".join([f"{r['country']} ({r['value']/1e6:.2f} млн)"
                           for _, r in top_d.iterrows()]) + ".",
        "tone": "rose",
    })

    # EU compensation
    eu_work = _last(df, "EUU", "SP.POP.1564.TO.ZS")
    eu_migr = _last(df, "EUU", "SM.POP.NETM")
    if eu_work[0] and eu_migr[0]:
        out.append({
            "title": "ЕС: компенсация миграцией",
            "text": f"Трудоспособное население ЕС - {eu_work[0]:.1f}%, "
                    f"чистая миграция за период - {eu_migr[0]/1e6:+.1f} млн. "
                    f"Миграция частично компенсирует снижение доли 15–64.",
            "tone": "amber",
        })
    return out


def economy_insights() -> list[dict]:
    df = D.load()
    out = []

    # correlation aging vs gdp per capita (latest year)
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    gdp = df[(df["indicator"] == "NY.GDP.PCAP.CD") & (~df["is_aggregate"])]
    ya, yg = age["year"].max(), gdp["year"].max()
    m = age[age["year"] == ya][["country_code", "value"]].merge(
        gdp[gdp["year"] == yg][["country_code", "value"]],
        on="country_code", suffixes=("_age", "_gdp"))
    if not m.empty:
        corr = m["value_age"].corr(m["value_gdp"].apply(lambda v: v if v > 0 else None))
        out.append({
            "title": "Старение ↔ богатство",
            "text": f"Корреляция доли 65+ и ВВП на душу: r = {corr:.2f}. "
                    f"Более богатые страны системно «старее» - это связано с лучшим "
                    f"здравоохранением и низкой рождаемостью.",
            "tone": "indigo",
        })

    # GDP growth in aging vs young countries
    pair_h = _first_and_last(df, "HIC", "NY.GDP.MKTP.KD.ZG", since=2010)
    pair_l = _first_and_last(df, "LIC", "NY.GDP.MKTP.KD.ZG", since=2010)
    if pair_h and pair_l:
        out.append({
            "title": "Темпы роста",
            "text": f"В развитых странах рост ВВП ({pair_h[1]['value']:.1f}% в "
                    f"{int(pair_h[1]['year'])}) ниже, чем в беднейших "
                    f"({pair_l[1]['value']:.1f}%). Старение тормозит экономику.",
            "tone": "rose",
        })

    # health spending vs aging
    hx = _last(df, "WLD", "SH.XPD.CHEX.GD.ZS")
    if hx[0]:
        out.append({
            "title": "Расходы на здравоохранение",
            "text": f"В мире - {hx[0]:.1f}% ВВП ({hx[1]} г.). С ростом доли 65+ "
                    f"расходы будут увеличиваться - это давление на бюджеты.",
            "tone": "pink",
        })

    # employment world trend
    pair = _first_and_last(df, "WLD", "SL.EMP.TOTL.SP.ZS", since=2000)
    if pair:
        a, b = pair
        out.append({
            "title": "Уровень занятости",
            "text": f"С {int(a['year'])} по {int(b['year'])} занятость в мире "
                    f"изменилась с {a['value']:.1f}% до {b['value']:.1f}% "
                    f"({b['value']-a['value']:+.1f} п.п.).",
            "tone": "emerald",
        })
    return out


def scenarios_insights() -> list[dict]:
    df = D.load()
    out = []

    # projected 65+ for WLD by 2050 (linear extrapolation)
    s = df[(df["country_code"] == "WLD") & (df["indicator"] == "SP.POP.65UP.TO.ZS")].sort_values("year")
    if len(s) >= 5:
        recent = s.tail(20)
        x = recent["year"].values
        y = recent["value"].values
        slope = (y[-1] - y[0]) / (x[-1] - x[0])
        proj = y[-1] + slope * (2050 - x[-1])
        out.append({
            "title": "Прогноз 2050: мир",
            "text": f"При сохранении тренда доля 65+ к 2050 г. достигнет ~{proj:.1f}% "
                    f"(сейчас {y[-1]:.1f}%). Это вызовет глубокую реформу пенсионных систем.",
            "tone": "amber",
        })

    # dev vs developing fertility
    hic_f = _last(df, "HIC", "SP.DYN.TFRT.IN")
    lic_f = _last(df, "LIC", "SP.DYN.TFRT.IN")
    if hic_f[0] and lic_f[0]:
        out.append({
            "title": "Рождаемость: разрыв",
            "text": f"Развитые страны: {hic_f[0]:.2f} ребёнка на женщину "
                    f"(ниже 2.1 - депопуляция). Низкий доход: {lic_f[0]:.2f} - "
                    f"высокий потенциал прироста.",
            "tone": "indigo",
        })

    # investment by group
    inv_h = _last(df, "HIC", "NE.GDI.TOTL.ZS")
    inv_l = _last(df, "LIC", "NE.GDI.TOTL.ZS")
    if inv_h[0] and inv_l[0]:
        out.append({
            "title": "Инвестиции (% ВВП)",
            "text": f"HIC: {inv_h[0]:.1f}%, LIC: {inv_l[0]:.1f}%. Старение "
                    f"усиливает потребление и снижает норму сбережений → меньше инвестиций.",
            "tone": "emerald",
        })

    out.append({
        "title": "Рекомендация",
        "text": "Устойчивый сценарий = рождаемость ≥ 1.8 + контролируемая миграция "
                "(0.3–0.5% от населения в год) + рост производительности через "
                "автоматизацию и образование.",
        "tone": "rose",
    })
    return out


def map_insights() -> list[dict]:
    df = D.load()
    out = []
    age = df[(df["indicator"] == "SP.POP.65UP.TO.ZS") & (~df["is_aggregate"])]
    yr = age["year"].max()
    latest = age[age["year"] == yr]
    out.append({
        "title": "Географическая концентрация",
        "text": f"В {int(yr)} г. медианная доля 65+ по странам выборки - "
                f"{latest['value'].median():.1f}%, максимум - {latest['value'].max():.1f}% "
                f"({latest.nlargest(1, 'value').iloc[0]['country']}).",
        "tone": "indigo",
    })

    migr = df[(df["indicator"] == "SM.POP.NETM") & (~df["is_aggregate"])]
    yr2 = migr["year"].max()
    latest2 = migr[migr["year"] == yr2]
    positive = (latest2["value"] > 0).sum()
    negative = (latest2["value"] < 0).sum()
    out.append({
        "title": "Карта миграции",
        "text": f"В {int(yr2)} г. {positive} стран имели положительную чистую миграцию, "
                f"{negative} - отрицательную. Реципиенты сосредоточены в Сев. Америке, "
                f"Зап. Европе и Заливе, доноры - в Юж. Азии и Лат. Америке.",
        "tone": "emerald",
    })
    return out


# ─── UI helper ───────────────────────────────────────────────────────────

TONE_TO_COLOR = {
    "indigo": "#5B6CFF",
    "emerald": "#10B981",
    "amber": "#F59E0B",
    "pink": "#EC4899",
    "rose": "#F43F5E",
    "violet": "#8B5CF6",
    "cyan": "#06B6D4",
}


def insight_card(item: dict) -> dbc.Col:
    return dbc.Col(
        html.Div(
            [
                html.Div(item["title"], className="insight-title"),
                html.Div(item["text"], className="insight-text"),
            ],
            className="insight-card",
            style={"--accent-color": TONE_TO_COLOR.get(item["tone"], "#5B6CFF")},
        ),
        lg=3, md=6, className="mb-3",
    )


def insights_row(items: list[dict]) -> dbc.Row:
    return dbc.Row(
        [insight_card(i) for i in items],
        className="g-3 mb-2 insights-row",
    )


def insights_section(items: list[dict]) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Выводы", className="section-eyebrow"),
                    html.H2("Что говорят данные", className="section-title"),
                ],
                className="section-heading",
            ),
            insights_row(items),
        ],
        className="insights-section",
    )
