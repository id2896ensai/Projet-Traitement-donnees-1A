import datetime

import pandas as pd

from src.Model.sports_catalogue import BADMINTON


def _jeux_gagnes(score_jeu) -> tuple:
    """Retourne (jeux_gagnes_j1, jeux_gagnes_j2) pour un jeu au format 'X-Y'."""
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
    """Convertit une ligne de badminton/match.csv en dict Match.

    Le badminton est un sport individuel.
    Requiert un dictionnaire de joueurs pre-charge {nom (str): Player}.
    Le score final correspond au nombre de jeux gagnes (ex: 2-1 ou 2-0).
    """

    def __init__(self, joueurs: dict) -> None:
        self.joueurs = joueurs

    def adapt(self, row: pd.Series) -> dict:
        nom_j1 = str(row["player_1"]).strip()
        nom_j2 = str(row["player_2"]).strip()

        joueur_1 = self.joueurs.get(nom_j1)
        joueur_2 = self.joueurs.get(nom_j2)

        if joueur_1 is None or joueur_2 is None:
            raise KeyError("Joueur introuvable dans le dictionnaire")

        # Comptage des jeux gagnes sur les 3 manches possibles
        score_1, score_2 = 0, 0
        for col in ["game_1_score", "game_2_score", "game_3_score"]:
            v1, v2 = _jeux_gagnes(row.get(col))
            score_1 += v1
            score_2 += v2

        return {
            "sport":               BADMINTON,
            "participant_1":       joueur_1,
            "participant_2":       joueur_2,
            "score_participant_1": score_1,
            "score_participant_2": score_2,
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
