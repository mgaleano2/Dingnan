import os
import pandas as pd
from ScraperFC.sofascore import Sofascore

s = Sofascore()

MATCHES = [
    (15657889, "Nantong Zhiyun"),
    (15657885, "Guangxi Hengchen"),
    (15657877, "Ningbo FC"),
    (15657868, "Shenzhen Juniors"),
    (15657854, "Yanbian Longding"),
    (15657898, "Dalian Kuncheng City")
]

def partidos():
    for mid, label in MATCHES:      #Split bucle en dos variables
        md = s.get_match_dict(mid)
        hs = md.get("homeScore") or {}
        as_ = md.get("awayScore") or {}
        print(f"{label} id={mid} | {md['homeTeam']['name']} {hs.get('current')} - {as_.get('current')} {md['awayTeam']['name']}")
        print(f"   round={md.get('roundInfo',{}).get('round')} | liga={md.get('tournament',{}).get('uniqueTournament',{}).get('name')}")

COLUMNAS = [
    "name", "position", "jerseyNumber", "minutesPlayed", "rating", "captain",
    # ataque
    "goals", "goalAssist", "expectedGoals", "expectedAssists",
    "totalShots", "onTargetScoringAttempt", "shotOffTarget", "blockedScoringAttempt",
    "bigChanceCreated", "bigChanceMissed", "keyPass", "totalCross", "accurateCross",
    # pases
    "totalPass", "accuratePass", "totalLongBalls", "accurateLongBalls",
    # defensa / duelos
    "wonTackle", "totalTackle", "interceptionWon", "totalClearance", "ballRecovery",
    "aerialWon", "aerialLost", "duelWon", "duelLost", "wonContest", "challengeLost",
    # posesión / disciplina
    "touches", "possessionLostCtrl", "dispossessed", "unsuccessfulTouch",
    "fouls", "wasFouled", "totalOffside",
]

def individual():
    partido = 15657898  # vs Yanbian
    df = s.scrape_player_match_stats(partido)  # para partidos s.get_match_dict
    df = df[df["teamName"] == "Jiangxi Dingnan United"]
    df = df.loc[:, ~df.columns.duplicated()]
    cols = [c for c in COLUMNAS if c in df.columns]
    df = df[cols]
    df = df.sort_values("minutesPlayed", ascending=False)
    df["match_id"] = partido
    print(df.to_string(index=False))
    df.to_csv("data/stats_15657898.csv", index=False)

if __name__ == "__main__":
    #    partidos()
    individual()




