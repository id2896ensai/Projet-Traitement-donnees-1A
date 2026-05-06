import datetime
import pandas as pd
from Model.sport import Sport

BADMINTON = Sport("Badminton", "volant", 1, "Sport individuel de raquette", False)


def _jeux_gagnes(score_jeu) -> tuple:
    """Retourne (jeux_gagnes_j1, jeux_gagnes_j2) pour un score au format 'X-Y'."""
    if pd.isna(score_jeu) or str(score_jeu).strip() == "":
        return 0, 0
    parties = str(score_jeu).strip().split("-")
    if len(parties) != 2:
        return 0, 0
    try:
        s1, s2 = int(parties[0]), int(parties[1])
        if s1 > s2:
            return 1, 0
        if s2 > s1:
            return 0, 1
    except ValueError:
        pass
    return 0, 0


class BadmintonMatchAdapter:
    """
    Convertit une ligne de badminton/match.csv en dict Match.

    Colonnes CSV : date, player_1, player_2, game_1_score, game_2_score, game_3_score

    Requiert un dict d'equipes pre-charge {full_name (str): Team}.
    Les Teams sont des equipes solo (1 joueur) creees par BadmintonTeamAdapter.
    Score = nombre de jeux gagnes sur les 3 manches possibles.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        nom_j1 = str(row["player_1"]).strip()
        nom_j2 = str(row["player_2"]).strip()

        team_1 = self.equipes.get(nom_j1)
        team_2 = self.equipes.get(nom_j2)

        if team_1 is None or team_2 is None:
            raise KeyError(f"Joueur introuvable : '{nom_j1}' ou '{nom_j2}'")

        score_1, score_2 = 0, 0
        for col in ["game_1_score", "game_2_score", "game_3_score"]:
            v1, v2 = _jeux_gagnes(row.get(col))
            score_1 += v1
            score_2 += v2

        return {
            "sport":        BADMINTON,
            "participants": [team_1, team_2],
            "scores":       {team_1: score_1, team_2: score_2},
            "date_match":   datetime.date.fromisoformat(str(row["date"])),
        }
