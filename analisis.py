import os
import pandas as pd
from ScraperFC.sofascore import Sofascore
s = Sofascore()

# Scrapeamos Dingnan United - league one de china utilizando sofascore

MATCHES = [
    (15657889, "Nantong Zhiyun"),
    (15657885, "Guangxi Hengchen"),
    (15657877, "Ningbo FC"),
    (15657868, "Shenzhen Juniors"),
    (15657854, "Yanbian Longding"),
    (15657898, "Dalian Kuncheng City")
]

def partidos():
    for mid, label in MATCHES:
        md = s.get_match_dict(mid)
        hs = md.get("homeScore") or {}
        as_ = md.get("awayScore") or {}
        print(f"{label} id={mid} | {md['homeTeam']['name']} {hs.get('current')} - {as_.get('current')} {md['awayTeam']['name']}")
        print(f"   round={md.get('roundInfo',{}).get('round')} | liga={md.get('tournament',{}).get('uniqueTournament',{}).get('name')}")

# scrapeamos partido

def individual():
    partido = 15657898  # vs Yanbian
    df = s.scrape_player_match_stats(partido)  # para partidos s.get_match_dict
    df = df[df["teamName"] == "Jiangxi Dingnan United"]
    print(df[["name", "teamName", "minutesPlayed", "rating"]].to_string(index=False))
    df["match_id"] = partido
    df.to_csv("data/stats_15657898.csv", index=False)
# Buscamos partidos
partidos()

# Rendimiento individual
individual()




