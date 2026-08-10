import glob
import pandas as pd

pd.set_option("display.float_format", lambda v: f"{v:.2f}")

# (ronda, rival, resultado de Dingnan)
METADATA = {
    15657854: (13, "Yanbian", "0-3"),
    15657868: (14, "Shenzhen", "3-3"),
    15657877: (15, "Ningbo", "0-1"),
    15657885: (16, "Guangxi", "4-4"),
    15657889: (17, "Nantong", "1-5"),
    15657898: (18, "Dalian", "2-1"),
}


def cargar():
    dfs = [pd.read_csv(f) for f in sorted(glob.glob("data/stats_*.csv"))]
    return pd.concat(dfs, ignore_index=True)


def limpiar(df):
    df["pos"] = df.iloc[:, df.columns.tolist().index("position")]
    df["expectedGoals"] = pd.to_numeric(df["expectedGoals"], errors="coerce")
    df.loc[df["expectedGoals"] > 5, "expectedGoals"] = None
    return df


def tabla_partidos(df):
    t = df.groupby("match_id").agg(
        rating=("rating", "mean"),
        xg=("expectedGoals", "sum"),
        tiros=("totalShots", "sum"),
        pases_clave=("keyPass", "sum"),
        goles=("goals", "sum"),
        jugadores=("minutesPlayed", lambda x: (x.fillna(0) > 0).sum()),
    ).reset_index()
    t["round"] = t["match_id"].map(lambda m: METADATA[m][0])
    t["rival"] = t["match_id"].map(lambda m: METADATA[m][1])
    t["resultado"] = t["match_id"].map(lambda m: METADATA[m][2])
    cols = ["match_id", "round", "rival", "resultado", "rating", "xg", "tiros", "goles", "pases_clave", "jugadores"]
    return t[cols].sort_values("round").round(2)


def tabla_jugadores(df):
    jugo = df[df["minutesPlayed"].fillna(0) > 0]
    t = jugo.groupby("id").agg(
        nombre=("name", "first"),
        pos=("pos", "first"),
        partidos=("match_id", "nunique"),
        minutos=("minutesPlayed", "sum"),
        rating=("rating", "mean"),
        goles=("goals", "sum"),
        asistencias=("goalAssist", "sum"),
        xg=("expectedGoals", "sum"),
        tiros=("totalShots", "sum"),
        pases_clave=("keyPass", "sum"),
        pases_prop_ok=("accurateOwnHalfPasses", "sum"),
        pases_prop_tot=("totalOwnHalfPasses", "sum"),
        pases_cc_ok=("accurateOppositionHalfPasses", "sum"),
        pases_cc_tot=("totalOppositionHalfPasses", "sum"),
        lb_ok=("accurateLongBalls", "sum"),
        lb_tot=("totalLongBalls", "sum"),
        duelos_gan=("duelWon", "sum"),
        duelos_per=("duelLost", "sum"),
        aereos_gan=("aerialWon", "sum"),
        aereos_per=("aerialLost", "sum"),
    ).reset_index()
    t["G_A"] = t["goles"] + t["asistencias"]

    t["pases_prop_err"] = t["pases_prop_tot"] - t["pases_prop_ok"]
    t["pct_prop"] = (t["pases_prop_ok"] / t["pases_prop_tot"] * 100).fillna(0)

    t["pases_cc_err"] = t["pases_cc_tot"] - t["pases_cc_ok"]
    t["pct_cc"] = (t["pases_cc_ok"] / t["pases_cc_tot"] * 100).fillna(0)

    t["lb_err"] = t["lb_tot"] - t["lb_ok"]
    t["pct_lb"] = (t["lb_ok"] / t["lb_tot"] * 100).fillna(0)

    t["duelos_tot"] = t["duelos_gan"] + t["duelos_per"]
    t["pct_duelos"] = (t["duelos_gan"] / t["duelos_tot"] * 100).fillna(0)

    t["aereos_tot"] = t["aereos_gan"] + t["aereos_per"]
    t["pct_aereos"] = (t["aereos_gan"] / t["aereos_tot"] * 100).fillna(0)

    prom = ["pases_prop_tot", "pases_prop_ok", "pases_prop_err",
            "pases_cc_tot", "pases_cc_ok", "pases_cc_err",
            "lb_tot", "lb_ok", "lb_err",
            "duelos_tot", "duelos_gan", "duelos_per",
            "aereos_tot", "aereos_gan", "aereos_per"]
    for col in prom:
        t[col] = t[col] / t["partidos"]

    cols = ["nombre", "pos", "partidos", "minutos", "rating", "goles", "asistencias", "G_A", "xg", "tiros", "pases_clave",
            "pases_prop_tot", "pases_prop_ok", "pases_prop_err", "pct_prop",
            "pases_cc_tot", "pases_cc_ok", "pases_cc_err", "pct_cc",
            "lb_tot", "lb_ok", "lb_err", "pct_lb",
            "duelos_tot", "duelos_gan", "duelos_per", "pct_duelos",
            "aereos_tot", "aereos_gan", "aereos_per", "pct_aereos"]
    return t[cols].sort_values("minutos", ascending=False).round(2)


def reporte(df):
    j = tabla_jugadores(df)
    cols = ["nombre", "pos", "partidos", "minutos", "rating", "goles", "asistencias", "G_A", "xg", "tiros",
            "pases_cc_tot", "pases_cc_ok", "pct_cc",
            "lb_tot", "lb_ok", "pct_lb",
            "duelos_tot", "duelos_gan", "pct_duelos",
            "aereos_tot", "aereos_gan", "pct_aereos"]
    r = j[j["partidos"] >= 2][cols].sort_values("rating", ascending=False)
    return r.reset_index(drop=True)


TRAD = {
    "nombre": "Jugador", "pos": "Pos", "partidos": "PJ", "minutos": "Min",
    "rating": "Rating", "goles": "Goles", "asistencias": "Asist.", "G_A": "G+A",
    "xg": "xG", "tiros": "Tiros", "pases_clave": "Pases clave",
    "pases_cc_tot": "Pases CC", "pases_cc_ok": "Pases CC OK", "pct_cc": "% CC",
    "lb_tot": "LB", "lb_ok": "LB OK", "pct_lb": "% LB",
    "duelos_tot": "Duelos", "duelos_gan": "Duelos gan.", "pct_duelos": "% Duelos",
    "aereos_tot": "Aéreos", "aereos_gan": "Aéreos gan.", "pct_aereos": "% Aéreos",
    "round": "Ronda", "rival": "Rival", "resultado": "Resultado",
}


def _md_tabla(df, cols):
    header = " | ".join(TRAD[c] for c in cols)
    sep = " | ".join(["---"] * len(cols))
    filas = []
    for _, r in df.iterrows():
        vals = []
        for c in cols:
            v = r[c]
            if isinstance(v, float):
                vals.append(f"{v:.2f}".replace(".00", ""))
            else:
                vals.append(str(v))
        filas.append("| " + " | ".join(vals) + " |")
    return "| " + header + " |\n| " + sep + " |\n" + "\n".join(filas)


def reporte_md(r, t):
    pos = {"D": "defensor", "M": "mediocampista", "F": "delantero", "G": "arquero"}
    p = lambda x: pos.get(x, x)

    top = r.iloc[0]
    goleador = r.sort_values(["goles", "rating"], ascending=False).iloc[0]
    g_a = r.sort_values(["G_A", "rating"], ascending=False).iloc[0]
    tirador = r.sort_values("tiros", ascending=False).iloc[0]
    xg_top = r.sort_values("xg", ascending=False).iloc[0]
    pasador = r.sort_values("pases_cc_tot", ascending=False).iloc[0]
    pct_pase = r[(r["partidos"] >= 3) & (r["pases_cc_tot"] >= 5)].sort_values("pct_cc", ascending=False).iloc[0]
    duelo = r.sort_values("duelos_tot", ascending=False).iloc[0]
    pct_duelo = r[(r["partidos"] >= 3) & (r["duelos_tot"] >= 3)].sort_values("pct_duelos", ascending=False).iloc[0]
    aereo = r.sort_values("aereos_tot", ascending=False).iloc[0]
    lb_top = r.sort_values("lb_tot", ascending=False).iloc[0]
    gks = r[r["pos"] == "G"].sort_values("rating", ascending=False)
    gk = gks.iloc[0] if not gks.empty else None

    v_win = (t["resultado"].map(lambda s: int(s.split("-")[0]) > int(s.split("-")[1]))).sum()
    v_draw = (t["resultado"].map(lambda s: int(s.split("-")[0]) == int(s.split("-")[1]))).sum()
    v_loss = len(t) - v_win - v_draw
    def p_n(n, word):
        return f"{n} {word}{'s' if n != 1 else ''}"

    L = []
    L.append("# Reporte de Rendimiento — Jiangxi Dingnan United")
    L.append("")
    L.append("**Chinese League 1 · Rondas 13 a 18 · Datos: Sofascore**")
    L.append("")
    L.append(f"Jiangxi Dingnan United jugó **{len(t)} partidos**: **{p_n(v_win, 'victoria')}, {p_n(v_draw, 'empate')}, {p_n(v_loss, 'derrota')}**. "
             f"La muestra es chica (6 partidos), así que pensá esto como una **primera señal**, no como una conclusión.")
    L.append("")
    L.append("## Resultados")
    L.append("")
    L.append(_md_tabla(t, ["round", "rival", "resultado", "rating", "xg", "tiros"]))
    L.append("")
    L.append("Los números hablan claro: cuando el equipo genera tiros (11+ por partido) suma puntos, y cuando no "
             "(R13 y R17, los peores partidos) pierde.")
    L.append("")
    L.append("## Top 10 — ranking por rating")
    L.append("")
    L.append(_md_tabla(r.head(10), ["nombre", "pos", "partidos", "minutos", "rating", "goles", "asistencias", "G_A", "xg", "tiros"]))
    L.append("")
    L.append("## Destacados")
    L.append("")
    L.append(f"- **Mejor rating**: **{top['nombre']}** ({top['rating']:.2f}, {p(top['pos'])}, {top['partidos']:.0f} PJ, {top['minutos']:.0f} min).")
    L.append(f"- **Goleador**: **{goleador['nombre']}** con {goleador['goles']:.0f} goles en {goleador['partidos']:.0f} PJ.")
    L.append(f"- **Más G+A**: **{g_a['nombre']}** ({g_a['G_A']:.0f} participaciones).")
    L.append(f"- **Más tiros**: **{tirador['nombre']}** con {tirador['tiros']:.0f} remates.")
    L.append(f"- **Mayor xG**: **{xg_top['nombre']}** ({xg_top['xg']:.2f} de gol esperado).")
    L.append(f"- **Distribuidor**: **{pasador['nombre']}** con {pasador['pases_cc_tot']:.0f} pases en campo contrario por partido.")
    L.append(f"- **Precisión de pase (CC)**: **{pct_pase['nombre']}** completa el {pct_pase['pct_cc']:.0f}% en campo contrario (mín. 3 PJ).")
    L.append(f"- **Rey de los duelos**: **{duelo['nombre']}** ({duelo['duelos_tot']:.0f} por partido, {duelo['pct_duelos']:.0f}% ganados).")
    L.append(f"- **Mejor % de duelos** (mín. 3 PJ): **{pct_duelo['nombre']}** con {pct_duelo['pct_duelos']:.0f}%.")
    L.append(f"- **Juego aéreo**: **{aereo['nombre']}** gana {aereo['aereos_tot']:.0f} aéreos por partido.")
    L.append(f"- **Pelota larga**: **{lb_top['nombre']}** con {lb_top['lb_tot']:.0f} long balls por partido.")
    if gk is not None:
        L.append(f"- **Mejor arquero**: **{gk['nombre']}** ({gk['rating']:.2f} de rating en {gk['partidos']:.0f} PJ).")
    L.append("")
    L.append("## Notas metodológicas")
    L.append("")
    L.append("- Los promedios son **por partido** (suma ÷ partidos jugados con minutos).")
    L.append("- Rating = **promedio simple** del rating que Sofascore le da a cada jugador en cada partido.")
    L.append("- Se **excluyeron jugadores con 1 solo partido** (muestra insuficiente).")
    L.append("- El xG fue **corregido**: la API devolvió un valor inválido (142.0) en un partido que se descartó.")
    L.append("- Posiciones: D = defensor, M = mediocampista, F = delantero, G = arquero.")
    L.append("")
    L.append("## Tabla completa")
    L.append("")
    L.append(_md_tabla(r, r.columns.tolist()))
    L.append("")

    md = "\n".join(L)
    with open("data/reporte.md", "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    df = limpiar(cargar())
    t = tabla_partidos(df)
    t.to_csv("data/tabla_partidos.csv", index=False)
    print(t.to_string(index=False))
    j = tabla_jugadores(df)
    j.to_csv("data/tabla_jugadores.csv", index=False)
    print("\n")
    print(j.to_string(index=False))
    r = reporte(df)
    r.to_csv("data/reporte.csv", index=False)
    print("\n=== REPORTE ===")
    print(r.to_string(index=False))
    reporte_md(r, t)
    print("\nreporte.md generado en data/")
