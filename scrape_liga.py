import json
import os
import time

import pandas as pd
from ScraperFC.sofascore import Sofascore

OUT_DIR = "data/liga"
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    with open("data/rounds.json", encoding="utf-8") as f:
        rounds = json.load(f)

    s = Sofascore()
    total = sum(len(v) for v in rounds.values())
    done = 0
    for ronda, partidos in rounds.items():
        for p in partidos:
            mid = p["id"]
            out = os.path.join(OUT_DIR, f"stats_{mid}.csv")
            if os.path.exists(out):
                done += 1
                continue
            try:
                df = s.scrape_player_match_stats(mid)
                df["match_id"] = mid
                df.to_csv(out, index=False)
            except Exception as e:
                print(f"  ERROR {mid}: {type(e).__name__}: {e}")
            done += 1
            print(f"[{done}/{total}] ronda {ronda} {p['home']} vs {p['away']} ({mid})")
            time.sleep(1)


if __name__ == "__main__":
    main()
