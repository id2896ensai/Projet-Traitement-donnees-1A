"""

Fonctions disponibles
─────────────────────
  plot_podium               — Barres horizontales, top-N par victoires
  plot_bilan_equipe         — Camembert V/D/N pour une équipe
  plot_gagnants_par_saison  — Timeline colorée : un point = une victoire
  plot_summary_tableau      — Tableau stylé couleurs conditionnelles
"""

import datetime
import plotly.graph_objects as go
from .stats import podium, stats_descriptives


def _vainqueur_match(match):
    """Retourne le participant gagnant d'un match, ou None si nul."""
    max_score = max(match.scores.values())
    gagnants = [p for p, s in match.scores.items() if s == max_score]
    return gagnants[0] if len(gagnants) == 1 else None


def _to_date(d):
    """Convertit datetime → date si besoin."""
    if isinstance(d, datetime.datetime):
        return d.date()
    return d

# 1. Podium — barres horizontales


def plot_podium(matches: list, sport_nom: str = "", n: int = 10) -> None:
    """Classement horizontal des n meilleures équipes par victoires."""
    classement = podium(matches, n=n)
    if not classement:
        print("  Pas assez de données pour afficher le podium.")
        return

    equipes = [t.full_name for t, _ in classement]
    victoires = [v for _, v in classement]

    palette_podium = ["#F5C518", "#A8A9AD", "#CD7F32"]
    couleurs = [palette_podium[i] if i < 3 else "#5B8DB8"
                for i in range(len(equipes))]

    # Inverser pour avoir le 1er en haut
    equipes_inv = equipes[::-1]
    victoires_inv = victoires[::-1]
    couleurs_inv = couleurs[::-1]

    fig = go.Figure(go.Bar(
        x=victoires_inv,
        y=equipes_inv,
        orientation="h",
        marker_color=couleurs_inv,
        text=victoires_inv,
        textposition="outside",
    ))

    titre = "Classement par victoires"
    if sport_nom:
        titre += f"  —  {sport_nom}"

    fig.update_layout(
        title=dict(text=titre, font=dict(size=16, color="#2C3E50")),
        xaxis_title="Nombre de victoires",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=max(400, len(equipes) * 45),
        xaxis=dict(gridcolor="#ebebeb"),
        margin=dict(l=20, r=40, t=60, b=40),
    )
    fig.show()


# 2. Bilan équipe — camembert V/D/N

def plot_bilan_equipe(matches: list, nom_equipe: str, sport_nom: str = "") -> None:
    """Camembert Victoires / Défaites / Nuls pour une équipe."""
    stats = stats_descriptives(matches, nom_equipe)
    if "erreur" in stats:
        print(f"  {stats['erreur']}")
        return

    labels_raw = ["Victoires", "Défaites", "Nuls"]
    valeurs_raw = [stats["nb_victoires"], stats["nb_defaites"], stats["nb_nuls"]]
    couleurs_raw = ["#2ECC71", "#E74C3C", "#95A5A6"]

    labels = [l for l, v in zip(labels_raw, valeurs_raw) if v > 0]  # noqa: E741
    valeurs = [v for v in valeurs_raw if v > 0]
    couleurs = [c for c, v in zip(couleurs_raw, valeurs_raw) if v > 0]

    if not valeurs:
        print("  Aucune donnée à afficher.")
        return

    titre = f"Bilan  —  {nom_equipe}"
    if sport_nom:
        titre += f"  ({sport_nom})"

    fig = go.Figure(go.Pie(
        labels=labels,
        values=valeurs,
        marker=dict(colors=couleurs, line=dict(color="white", width=2)),
        textinfo="label+percent+value",
        hoverinfo="label+value+percent",
    ))

    fig.update_layout(
        title=dict(text=titre, font=dict(size=16, color="#2C3E50")),
        annotations=[dict(
            text=(
                f"{stats['nb_matchs']} matchs joués  |  "
                f"Taux de victoire : {stats['pct_victoires']} %"
            ),
            x=0.5, y=-0.1, showarrow=False,
            font=dict(size=11, color="#555555"),
            xref="paper", yref="paper",
        )],
        height=500,
        margin=dict(t=80, b=80),
    )
    fig.show()


# 4. Tableau summary — classement général stylé


def plot_summary_tableau(matches: list, sport_nom: str = "", top_n: int = 15) -> None:
    """
    Tableau plotly stylé : J / V / D / N / %V / Moy+ / Moy− / Net
    ─ %V  : dégradé Rouge→Jaune→Vert
    ─ Net : dégradé Rouge→Bleu
    ─ Top 3 : Or / Argent / Bronze
    """
    equipes_vues: set[str] = set()
    for m in matches:
        for t in m.participants:
            if t.full_name:
                equipes_vues.add(t.full_name)

    lignes = []
    for nom in equipes_vues:
        s = stats_descriptives(matches, nom)
        if "erreur" in s or s["nb_matchs"] == 0:
            continue
        net = round(s["moy_pts_marques"] - s["moy_pts_encaisses"], 2)
        lignes.append({
            "Équipe":  nom,
            "J":       s["nb_matchs"],
            "V":       s["nb_victoires"],
            "D":       s["nb_defaites"],
            "N":       s["nb_nuls"],
            "%V":      s["pct_victoires"],
            "Moy +":   s["moy_pts_marques"],
            "Moy −":   s["moy_pts_encaisses"],
            "Net":     net,
        })

    if not lignes:
        print("  Pas assez de données pour le tableau.")
        return

    lignes.sort(key=lambda r: (r["%V"], r["Net"]), reverse=True)
    lignes = lignes[:top_n]

    MEDAILLES = {0: "#F5C518", 1: "#A8A9AD", 2: "#CD7F32"}

    rangs = [str(i + 1) for i in range(len(lignes))]
    equipes = [r["Équipe"][:28] for r in lignes]
    j_vals = [str(r["J"]) for r in lignes]
    v_vals = [str(r["V"]) for r in lignes]
    d_vals = [str(r["D"]) for r in lignes]
    n_vals = [str(r["N"]) for r in lignes]
    pct_vals = [f"{r['%V']:.1f}" for r in lignes]
    moy_plus = [f"{r['Moy +']:.1f}" for r in lignes]
    moy_moins = [f"{r['Moy −']:.1f}" for r in lignes]
    net_vals = [f"{r['Net']:+.1f}" for r in lignes]

    pct_raw = [r["%V"] for r in lignes]
    pct_min, pct_max = min(pct_raw), max(pct_raw)
    pct_colors = [
        f"rgba({int(255 * (1 - (v - pct_min) / max(pct_max - pct_min, 1)))}, "
        f"{int(200 * (v - pct_min) / max(pct_max - pct_min, 1) + 55)}, 50, 0.7)"
        for v in pct_raw
    ]

    net_raw = [r["Net"] for r in lignes]
    net_colors = [
        "rgba(52, 152, 219, 0.6)" if v >= 0 else "rgba(231, 76, 60, 0.6)"
        for v in net_raw
    ]

    rang_colors = [MEDAILLES.get(i, "#F8F9FA") for i in range(len(lignes))]
    row_colors = ["#F8F9FA" if i % 2 == 0 else "#FFFFFF" for i in range(len(lignes))]

    fig = go.Figure(go.Table(
        header=dict(
            values=["<b>#</b>", "<b>Équipe</b>", "<b>J</b>", "<b>V</b>",
                    "<b>D</b>", "<b>N</b>", "<b>%V</b>",
                    "<b>Moy +</b>", "<b>Moy −</b>", "<b>Net</b>"],
            fill_color="#2C3E50",
            font=dict(color="white", size=12),
            align="center",
            height=35,
        ),
        cells=dict(
            values=[rangs, equipes, j_vals, v_vals, d_vals, n_vals,
                    pct_vals, moy_plus, moy_moins, net_vals],
            fill_color=[rang_colors, row_colors, row_colors, row_colors,
                        row_colors, row_colors, pct_colors,
                        row_colors, row_colors, net_colors],
            font=dict(color="#2C3E50", size=11),
            align=["center", "left"] + ["center"] * 8,
            height=30,
        ),
    ))

    titre = "Classement général"
    if sport_nom:
        titre += f"  —  {sport_nom}"

    fig.update_layout(
        title=dict(text=titre, font=dict(size=16, color="#2C3E50")),
        height=max(400, len(lignes) * 35 + 120),
        margin=dict(t=80, b=60),
        annotations=[dict(
            text=(
                "J = matchs joués  |  V = Victoires  |  D = Défaites  |  N = Nuls  |  "
                "Moy + = pts marqués/match  |  Moy − = pts encaissés/match"
            ),
            x=0.5, y=-0.05, showarrow=False,
            font=dict(size=10, color="#555555"),
            xref="paper", yref="paper",
        )],
    )
    fig.show()
