"""

Fonctions disponibles
─────────────────────
  plot_podium               — Barres horizontales, top-N par victoires
  plot_bilan_equipe         — Camembert V/D/N pour une équipe
  plot_gagnants_par_saison  — Timeline colorée : un point = une victoire
  plot_summary_tableau      — Tableau stylé couleurs conditionnelles
  autre chose peut etre
"""

import datetime
from collections import defaultdict

import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from .stats import podium, stats_descriptives, matchs_equipe


# ══════════════════════════════════════════════════════════════════
# Helpers internes
# ══════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════
# 1. Podium — barres horizontales
# ══════════════════════════════════════════════════════════════════

def plot_podium(matches: list, sport_nom: str = "", n: int = 10) -> None:
    """Classement horizontal des n meilleures équipes par victoires."""
    classement = podium(matches, n=n)
    if not classement:
        print("  Pas assez de données pour afficher le podium.")
        return

    equipes  = [t.full_name for t, _ in classement]
    victoires = [v for _, v in classement]

    palette_podium = ["#F5C518", "#A8A9AD", "#CD7F32"]
    couleurs = [palette_podium[i] if i < 3 else "#5B8DB8"
                for i in range(len(equipes))]

    fig, ax = plt.subplots(figsize=(9, max(4, len(equipes) * 0.55)))
    positions = list(range(len(equipes) - 1, -1, -1))

    bars = ax.barh(positions, victoires, color=couleurs,
                   height=0.6, edgecolor="white", linewidth=0.8)

    for bar, val in zip(bars, victoires):
        ax.text(
            bar.get_width() + max(victoires) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center", ha="left", fontsize=10,
            fontweight="bold", color="#333333",
        )

    ax.set_yticks(positions)
    ax.set_yticklabels(equipes, fontsize=10)
    ax.set_xlabel("Nombre de victoires", fontsize=10)
    ax.set_xlim(0, max(victoires) * 1.15)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    titre = "Classement par victoires"
    if sport_nom:
        titre += f"  —  {sport_nom}"
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=14)

    legende = [
        mpatches.Patch(color="#F5C518", label="1er"),
        mpatches.Patch(color="#A8A9AD", label="2ème"),
        mpatches.Patch(color="#CD7F32", label="3ème"),
    ]
    if len(equipes) > 3:
        legende.append(mpatches.Patch(color="#5B8DB8", label="Autres"))
    ax.legend(handles=legende, fontsize=9, loc="lower right")

    ax.xaxis.grid(True, linestyle="--", alpha=0.4, color="gray")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.show()


# ══════════════════════════════════════════════════════════════════
# 2. Bilan équipe — camembert V/D/N
# ══════════════════════════════════════════════════════════════════

def plot_bilan_equipe(matches: list, nom_equipe: str, sport_nom: str = "") -> None:
    """Camembert Victoires / Défaites / Nuls pour une équipe."""
    stats = stats_descriptives(matches, nom_equipe)
    if "erreur" in stats:
        print(f"  {stats['erreur']}")
        return

    labels_raw   = ["Victoires", "Défaites", "Nuls"]
    valeurs_raw  = [stats["nb_victoires"], stats["nb_defaites"], stats["nb_nuls"]]
    couleurs_raw = ["#2ECC71", "#E74C3C", "#95A5A6"]

    labels   = [l for l, v in zip(labels_raw,   valeurs_raw) if v > 0]
    valeurs  = [v for v in valeurs_raw if v > 0]
    couleurs = [c for c, v in zip(couleurs_raw, valeurs_raw) if v > 0]

    if not valeurs:
        print("  Aucune donnée à afficher.")
        return

    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        valeurs,
        labels=labels,
        colors=couleurs,
        autopct=lambda p: f"{p:.1f}%\n({int(round(p * sum(valeurs) / 100))})",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 11},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
        at.set_color("white")

    titre = f"Bilan  —  {nom_equipe}"
    if sport_nom:
        titre += f"  ({sport_nom})"
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=16)
    fig.text(
        0.5, 0.02,
        f"{stats['nb_matchs']} matchs joués  |  "
        f"Taux de victoire : {stats['pct_victoires']} %",
        ha="center", fontsize=10, color="#555555",
    )
    ax.axis("equal")
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()


# ══════════════════════════════════════════════════════════════════
# 3. Timeline gagnants — un point par victoire, coloré par équipe
# ══════════════════════════════════════════════════════════════════

def plot_gagnants_par_saison(matches: list, sport_nom: str = "") -> None:
    """
    Timeline horizontale : chaque victoire = un point coloré.
    Axe X = date du match  |  Axe Y = équipe gagnante
    Les équipes sont triées du bas (moins de victoires) vers le haut (plus).
    Fonctionne pour tout sport disposant d'une date_match.
    """
    # ── Collecte ───────────────────────────────────────────────
    points = []          # liste de (date, full_name_gagnant)
    for m in matches:
        date = getattr(m, "date_match", None)
        if date is None:
            continue
        gagnant = _vainqueur_match(m)
        if gagnant is None:
            continue
        points.append((_to_date(date), gagnant.full_name))

    if not points:
        print("  Pas de données exploitables pour la timeline.")
        return

    # ── Palette : une couleur par équipe ───────────────────────
    equipes_uniques = sorted({g for _, g in points})
    nb_eq = len(equipes_uniques)

    if nb_eq <= 10:
        base_colors = list(plt.cm.tab10.colors)
    elif nb_eq <= 20:
        base_colors = list(plt.cm.tab20.colors)
    else:
        base_colors = [plt.cm.hsv(i / nb_eq) for i in range(nb_eq)]

    couleur_eq = {eq: base_colors[i % len(base_colors)]
                  for i, eq in enumerate(equipes_uniques)}

    # ── Tri des équipes par nb victoires (plus haut = plus de victoires) ─
    compte = defaultdict(int)
    for _, g in points:
        compte[g] += 1
    equipes_triees = sorted(equipes_uniques, key=lambda e: compte[e])
    y_pos = {eq: i for i, eq in enumerate(equipes_triees)}

    # ── Figure ─────────────────────────────────────────────────
    hauteur = max(5, nb_eq * 0.40)
    fig, ax = plt.subplots(figsize=(14, hauteur))

    # Lignes de fond
    for i in range(len(equipes_triees)):
        ax.axhline(i, color="#ebebeb", linewidth=0.7, zorder=0)

    # Points
    dates = [p[0] for p in points]
    ys    = [y_pos[p[1]] for p in points]
    cols  = [couleur_eq[p[1]] for p in points]
    ax.scatter(dates, ys, c=cols, s=30, alpha=0.78, linewidths=0, zorder=2)

    # Étiquettes Y  (nom + nb victoires)
    fontsize_y = max(6, min(9, 130 // max(nb_eq, 1)))
    ax.set_yticks(range(len(equipes_triees)))
    ax.set_yticklabels(
        [f"{eq}  ({compte[eq]})" for eq in equipes_triees],
        fontsize=fontsize_y,
    )
    ax.yaxis.set_tick_params(length=0)

    # Axe X : dates
    ax.xaxis_date()
    fig.autofmt_xdate(rotation=30, ha="right")
    ax.set_xlabel("Date", fontsize=10)

    titre = "Gagnants par match — timeline"
    if sport_nom:
        titre += f"  |  {sport_nom}"
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=14)

    # Légende latérale (seulement si le nombre d'équipes reste lisible)
    if nb_eq <= 16:
        legende = [
            mpatches.Patch(color=couleur_eq[eq], label=eq)
            for eq in reversed(equipes_triees)
        ]
        ax.legend(
            handles=legende, fontsize=7,
            loc="upper left", bbox_to_anchor=(1.01, 1),
            borderaxespad=0, title="Équipes", title_fontsize=8,
        )
        plt.tight_layout(rect=[0, 0, 0.82, 1])
    else:
        plt.tight_layout()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.show()


# ══════════════════════════════════════════════════════════════════
# 4. Tableau summary — classement général stylé
# ══════════════════════════════════════════════════════════════════

def plot_summary_tableau(matches: list, sport_nom: str = "", top_n: int = 15) -> None:
    """
    Tableau matplotlib stylé : J / V / D / N / %V / Moy+ / Moy− / Net
    ─ %V  : dégradé Rouge→Jaune→Vert selon la valeur relative
    ─ Net : dégradé Rouge→Bleu selon la valeur relative
    ─ Top 3 : numéro en Or / Argent / Bronze
    """
    # ── Collecte de toutes les équipes présentes ───────────────
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
            "%V":      s["pct_victoires"],          # déjà un float
            "Moy +":   s["moy_pts_marques"],        # déjà un float
            "Moy −":   s["moy_pts_encaisses"],      # déjà un float
            "Net":     net,
        })

    if not lignes:
        print("  Pas assez de données pour le tableau.")
        return

    # Tri : %V décroissant, puis Net décroissant
    lignes.sort(key=lambda r: (r["%V"], r["Net"]), reverse=True)
    lignes = lignes[:top_n]

    # ── Données textuelles ─────────────────────────────────────
    colonnes = ["#", "Équipe", "J", "V", "D", "N", "%V", "Moy +", "Moy −", "Net"]
    rows = []
    for rang, r in enumerate(lignes, 1):
        rows.append([
            str(rang),
            r["Équipe"][:28],
            str(r["J"]),
            str(r["V"]),
            str(r["D"]),
            str(r["N"]),
            f"{r['%V']:.1f}",
            f"{r['Moy +']:.1f}",
            f"{r['Moy −']:.1f}",
            f"{r['Net']:+.1f}",
        ])

    # ── Figure ─────────────────────────────────────────────────
    nb_lignes  = len(rows)
    hauteur_fig = max(3.5, nb_lignes * 0.44 + 1.4)
    fig, ax = plt.subplots(figsize=(13, hauteur_fig))
    ax.axis("off")

    titre = "Classement général"
    if sport_nom:
        titre += f"  —  {sport_nom}"
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=10)

    table = ax.table(
        cellText=rows,
        colLabels=colonnes,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.6)

    # ── Constantes de couleurs ─────────────────────────────────
    HEADER_BG  = "#2C3E50"
    HEADER_FG  = "white"
    ROW_ODD    = "#F8F9FA"
    ROW_EVEN   = "#FFFFFF"
    BORDER_COL = "#DEE2E6"
    MEDAILLES  = {1: "#F5C518", 2: "#A8A9AD", 3: "#CD7F32"}

    # Normalisation pour les gradients
    pct_vals = [r["%V"] for r in lignes]
    net_vals  = [r["Net"]  for r in lignes]
    pct_min, pct_max = min(pct_vals), max(pct_vals)
    net_min,  net_max  = min(net_vals),  max(net_vals)

    def _norm(val, vmin, vmax):
        return 0.5 if vmax == vmin else (val - vmin) / (vmax - vmin)

    cmap_green = cm.get_cmap("RdYlGn")
    cmap_blue  = cm.get_cmap("RdBu")

    def _luminance(rgba):
        return 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]

    col_pct  = colonnes.index("%V")
    col_net  = colonnes.index("Net")
    col_eq   = colonnes.index("Équipe")
    col_rang = colonnes.index("#")

    # ── Colorisation cellule par cellule ──────────────────────
    for (row_i, col_j), cell in table.get_celld().items():
        cell.set_edgecolor(BORDER_COL)
        cell.set_linewidth(0.5)

        if row_i == 0:
            # En-tête
            cell.set_facecolor(HEADER_BG)
            cell.set_text_props(color=HEADER_FG, fontweight="bold")
            continue

        data = lignes[row_i - 1]
        bg   = ROW_ODD if row_i % 2 == 1 else ROW_EVEN

        if col_j == col_rang and row_i in MEDAILLES:
            cell.set_facecolor(MEDAILLES[row_i])
            cell.set_text_props(fontweight="bold", color="#333333")

        elif col_j == col_eq:
            cell.set_facecolor(bg)
            cell.set_text_props(ha="left", fontweight="bold", color="#2C3E50")
            cell.PAD = 0.05

        elif col_j == col_pct:
            rgba = cmap_green(_norm(data["%V"], pct_min, pct_max))
            cell.set_facecolor(rgba)
            cell.set_text_props(
                fontweight="bold",
                color="white" if _luminance(rgba) < 0.5 else "#222222",
            )

        elif col_j == col_net:
            rgba = cmap_blue(_norm(data["Net"], net_min, net_max))
            cell.set_facecolor(rgba)
            cell.set_text_props(
                fontweight="bold",
                color="white" if _luminance(rgba) < 0.5 else "#222222",
            )

        else:
            cell.set_facecolor(bg)
        # Légende des abréviations
    fig.text(
        0.5, 0.02,
        "J = nombre total de matchs joués par l’équipe   |   V = Victoires   |   D = Défaites   |   N = Nuls | Moy + = moyenne de points marqués par match | Moy − = moyenne de points encaissés par match ",
        ha="center",
        fontsize=9,
        color="#555555",
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()
