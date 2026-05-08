# Fonctions d'analyse et de statistiques sur les matchs.
from collections import defaultdict


def _vainqueur(match):
    """Retourne le vainqueur du match (score le plus élevé), ou None si égalité."""
    max_score = max(match.scores.values())
    vainqueurs = [p for p, s in match.scores.items() if s == max_score]
    if len(vainqueurs) == 1:
        return vainqueurs[0]
    return None  # égalité


def podium(matches: list, n: int = 3) -> list:
    """
    Classement des n premières équipes/joueurs par nombre de victoires.
    Retourne une liste de tuples (Team, nb_victoires) triée par ordre décroissant.
    """
    victoires = defaultdict(int)
    for m in matches:
        gagnant = _vainqueur(m)
        if gagnant is not None:
            victoires[gagnant] += 1

    classement = sorted(victoires.items(), key=lambda x: x[1], reverse=True)
    return classement[:n]


def victoires_equipe(matches: list, nom_equipe: str) -> int:
    """
    Nombre de victoires d'une équipe identifiée par son full_name (insensible à la casse).
    """
    nom_lower = nom_equipe.lower()
    total = 0
    for m in matches:
        for participant in m.participants:
            if participant.full_name and participant.full_name.lower() == nom_lower:
                if _vainqueur(m) == participant:
                    total += 1
    return total


def matchs_equipe(matches: list, nom_equipe: str) -> list:
    """Tous les matchs où l'équipe participe, identifiée par full_name."""
    nom_lower = nom_equipe.lower()
    resultat = []
    for m in matches:
        for participant in m.participants:
            if participant.full_name and participant.full_name.lower() == nom_lower:
                resultat.append(m)
                break
    return resultat


def matchs_joueur(matches: list, query: str, _prenom: str = "") -> list:
    """
    Matchs impliquant un joueur dont le nom correspond à la requête.

    query peut être :
      - un nom complet  "Gurel Ediz"
      - un prénom seul  "Gurel"
      - un nom seul     "Ediz"
      - une partie du nom (recherche partielle insensible à la casse)

    _prenom est conservé pour compatibilité ascendante (ignoré si query suffit).
    """
    q = query.strip().lower()
    # Si l'appelant a passé nom+prenom séparément, on les combine
    if _prenom:
        q_alt = (_prenom + " " + query).strip().lower()
    else:
        q_alt = ""

    def _correspond(p) -> bool:
        nom_p = (p.nom or "").lower()
        prenom_p = (p.prenom or "").lower()
        pseudo_p = (getattr(p, "pseudo", None) or "").lower()
        plein = f"{prenom_p} {nom_p}".strip()
        plein2 = f"{nom_p} {prenom_p}".strip()
        return (
            q in nom_p or q in prenom_p or q in pseudo_p
            or q in plein or q in plein2
            or (q_alt and (q_alt in plein or q_alt in plein2))
        )

    def _team_correspond(team) -> bool:
        full = (getattr(team, "full_name", None) or "").lower()
        if q in full or (q_alt and q_alt in full):
            return True
        return any(_correspond(p) for p in team.players)

    return [m for m in matches if any(_team_correspond(t) for t in m.participants)]


def stats_descriptives(matches: list, nom_equipe: str) -> dict:
    """
    Statistiques descriptives pour une équipe (adaptées aux sports collectifs).

    Retourne un dict avec :
      nb_matchs, nb_victoires, nb_defaites, nb_nuls, pct_victoires,
      moy_pts_marques, moy_pts_encaisses, max_score, min_score.
    """
    matchs_j = matchs_equipe(matches, nom_equipe)

    if not matchs_j:
        return {"erreur": f"Aucun match trouve pour '{nom_equipe}'"}

    nom_lower = nom_equipe.lower()
    nb_v = nb_d = nb_n = 0
    scores_m = []
    scores_e = []

    for m in matchs_j:
        equipe = next(
            (p for p in m.participants if p.full_name and p.full_name.lower() == nom_lower),
            None
        )
        if equipe is None:
            continue

        adversaire = next((p for p in m.participants if p != equipe), None)
        score_m = m.scores.get(equipe, 0)
        score_e = m.scores.get(adversaire, 0) if adversaire else 0

        scores_m.append(score_m)
        scores_e.append(score_e)

        gagnant = _vainqueur(m)
        if gagnant == equipe:
            nb_v += 1
        elif gagnant is None:
            nb_n += 1
        else:
            nb_d += 1

    n = len(scores_m) or 1  # évite division par zéro
    return {
        "nb_matchs":         len(matchs_j),
        "nb_victoires":      nb_v,
        "nb_defaites":       nb_d,
        "nb_nuls":           nb_n,
        "pct_victoires":     round(100 * nb_v / len(matchs_j), 1),
        "moy_pts_marques":   round(sum(scores_m) / n, 2),
        "moy_pts_encaisses": round(sum(scores_e) / n, 2),
        "max_score":         max(scores_m) if scores_m else 0,
        "min_score":         min(scores_m) if scores_m else 0,
    }
