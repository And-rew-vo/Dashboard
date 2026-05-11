"""Загружает реальные данные World Bank API одним запросом на индикатор
для всех стран сразу, сохраняет в data/wb_data.csv.

Запускается один раз:
    python data_fetch.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

INDICATORS = [
    "SP.POP.TOTL", "SP.POP.65UP.TO.ZS", "SP.POP.1564.TO.ZS",
    "SP.POP.0014.TO.ZS", "SP.POP.DPND", "SP.POP.DPND.OL", "SP.POP.DPND.YG",
    "SM.POP.NETM", "NY.GDP.MKTP.KD.ZG", "NY.GDP.PCAP.CD",
    "SL.EMP.TOTL.SP.ZS", "SL.TLF.CACT.ZS", "SH.XPD.CHEX.GD.ZS",
    "SP.DYN.LE00.IN", "SP.DYN.TFRT.IN",
    "NE.CON.GOVT.ZS", "SL.UEM.TOTL.ZS",
    "NV.IND.MANF.ZS", "NV.SRV.TOTL.ZS", "NV.AGR.TOTL.ZS",
    "NE.GDI.TOTL.ZS",
]

COUNTRIES = [
    "USA","CAN","GBR","DEU","FRA","ITA","ESP","JPN","KOR","AUS",
    "RUS","CHN","IND","BRA","MEX","ZAF","NGA","EGY","TUR","IDN",
    "VNM","PHL","SAU","ARE","UKR","POL","ROU","KAZ","ARG","COL",
    "IRN","PAK","BGD","ETH","KEN","THA","MYS","NLD","BEL","SWE",
    "NOR","FIN","CHE","AUT","PRT","GRC","IRL","ISR","NZL","SGP",
    "BLR","UZB","AZE","GEO","ARM","MDA","HUN","CZE","SVK","BGR",
]

AGGREGATES = ["WLD","EUU","ECS","NAC","EAS","SAS","LCN","MEA","SSF",
              "HIC","UMC","LMC","LIC"]

# WB API возвращает разные ID для агрегатов в эндпоинтах indicator vs country.
CODE_REMAP = {"XD": "HIC", "XM": "LIC", "XN": "LMC", "XT": "UMC"}


def log(msg: str):
    print(msg, flush=True)


def fetch_indicator(indicator: str) -> list[dict]:
    """Одним запросом по всем странам и агрегатам."""
    codes = ";".join(COUNTRIES + AGGREGATES)
    url = f"https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}"
    params = {"format": "json", "per_page": 30000, "date": "1990:2024"}
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, timeout=60)
            if r.status_code == 200:
                data = r.json()
                if len(data) >= 2 and data[1]:
                    return data[1]
            log(f"  HTTP {r.status_code}, retry {attempt}")
            time.sleep(2)
        except Exception as e:
            log(f"  exc {e}, retry {attempt}")
            time.sleep(3)
    return []


def fetch_country_meta() -> pd.DataFrame:
    all_codes = ";".join(COUNTRIES + AGGREGATES)
    url = f"https://api.worldbank.org/v2/country/{all_codes}"
    r = requests.get(url, params={"format": "json", "per_page": 500}, timeout=60)
    rows = []
    for c in r.json()[1]:
        rows.append({
            "country_code": c["id"],
            "country": c["name"],
            "region": c["region"]["value"],
            "income_group": c["incomeLevel"]["value"],
        })
    return pd.DataFrame(rows)


def main():
    log("Метаданные стран...")
    meta = fetch_country_meta()
    meta.to_csv(DATA_DIR / "countries.csv", index=False, encoding="utf-8-sig")
    log(f"  {len(meta)} записей")

    records = []
    for i, ind in enumerate(INDICATORS, 1):
        log(f"[{i}/{len(INDICATORS)}] {ind}")
        rows = fetch_indicator(ind)
        log(f"  получено {len(rows)} строк")
        for row in rows:
            if row.get("value") is None:
                continue
            raw_code = row["countryiso3code"] or row["country"]["id"]
            code = CODE_REMAP.get(row["country"]["id"], raw_code) or raw_code
            records.append({
                "country_code": code,
                "country": row["country"]["value"],
                "indicator": ind,
                "year": int(row["date"]),
                "value": row["value"],
            })

    df = pd.DataFrame(records)
    df = df.merge(meta[["country_code", "region", "income_group"]],
                  on="country_code", how="left")
    out = DATA_DIR / "wb_data.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    log(f"Сохранено: {out} ({len(df)} строк)")


if __name__ == "__main__":
    main()
