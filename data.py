"""Загрузка и подготовка данных World Bank для дашборда."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

INDICATOR_LABELS = {
    "SP.POP.TOTL": "Население, всего",
    "SP.POP.65UP.TO.ZS": "Доля 65+ (%)",
    "SP.POP.1564.TO.ZS": "Доля 15–64 (%)",
    "SP.POP.0014.TO.ZS": "Доля 0–14 (%)",
    "SP.POP.DPND": "Демографическая нагрузка",
    "SP.POP.DPND.OL": "Нагрузка пожилыми",
    "SP.POP.DPND.YG": "Нагрузка детьми",
    "SM.POP.NETM": "Чистая миграция",
    "NY.GDP.MKTP.KD.ZG": "Рост ВВП (%)",
    "NY.GDP.PCAP.CD": "ВВП на душу ($)",
    "SL.EMP.TOTL.SP.ZS": "Уровень занятости (%)",
    "SL.TLF.CACT.ZS": "Участие в рабсиле (%)",
    "SH.XPD.CHEX.GD.ZS": "Расходы на здравоохр. (% ВВП)",
    "SP.DYN.LE00.IN": "Ожид. продолжит. жизни",
    "SP.DYN.TFRT.IN": "Коэф. рождаемости",
    "NE.CON.GOVT.ZS": "Госрасходы (% ВВП)",
    "SL.UEM.TOTL.ZS": "Безработица (%)",
    "NV.IND.MANF.ZS": "Доля промышл. в ВВП (%)",
    "NV.SRV.TOTL.ZS": "Доля услуг в ВВП (%)",
    "NV.AGR.TOTL.ZS": "Доля с/х в ВВП (%)",
    "NE.GDI.TOTL.ZS": "Инвестиции (% ВВП)",
}

AGGREGATE_CODES = {"WLD", "EUU", "ECS", "NAC", "EAS", "SAS", "LCN", "MEA",
                   "SSF", "HIC", "UMC", "LMC", "LIC"}


@lru_cache(maxsize=1)
def load() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "wb_data.csv")
    df["year"] = df["year"].astype(int)
    df["is_aggregate"] = df["country_code"].isin(AGGREGATE_CODES)
    return df


@lru_cache(maxsize=1)
def countries() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "countries.csv")


def pivot(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index=["country_code", "country", "year"],
                          columns="indicator", values="value").reset_index()


def by_indicator(indicator: str, *, only_countries: bool = True,
                 only_aggregates: bool = False) -> pd.DataFrame:
    df = load()
    df = df[df["indicator"] == indicator]
    if only_countries:
        df = df[~df["is_aggregate"]]
    if only_aggregates:
        df = df[df["is_aggregate"]]
    return df


def latest_year(indicator: str) -> int:
    s = by_indicator(indicator)
    return int(s["year"].max())


def latest_value(country: str, indicator: str) -> float | None:
    df = load()
    s = df[(df["country_code"] == country) & (df["indicator"] == indicator)]
    if s.empty:
        return None
    return float(s.sort_values("year").iloc[-1]["value"])


COUNTRY_OPTIONS_CACHE: list[dict] | None = None


def country_options(include_aggregates: bool = True) -> list[dict]:
    df = load()
    sub = df[["country_code", "country", "is_aggregate"]].drop_duplicates()
    if not include_aggregates:
        sub = sub[~sub["is_aggregate"]]
    sub = sub.sort_values(["is_aggregate", "country"], ascending=[False, True])
    return [{"label": r["country"], "value": r["country_code"]}
            for _, r in sub.iterrows()]


def region_options() -> list[dict]:
    df = load()
    regs = sorted(df["region"].dropna().unique().tolist())
    return [{"label": r, "value": r} for r in regs if r and r != "Aggregates"]
