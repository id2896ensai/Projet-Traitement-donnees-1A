import datetime

import pandas as pd

from src.Model.sports_catalogue import TENNIS


class TennisMatchAdapter:
    """Convertit une ligne ATP ou WTA match CSV en dict Match.

    Le tennis est un sport individuel : deux joueurs s'affrontent.
    Requiert un dictionnaire de joueurs pre-charge {player_id (int): Player}.
    Score : 1 pour le vainqueur, 0 pour le perdant.
    """

    def __init__(self, joueurs: dict) -> None:
        self.joueurs = joueurs

    def adapt(self, row: pd.Series) -> dict:
        joueur_gagnant = self.joueurs.get(int(row["winner_id"]))
        joueur_perdant = self.joueurs.get(int(row["loser_id"]))

        if joueur_gagnant is None or joueur_perdant is None:
            raise KeyError("Joueur introuvable dans le dictionnaire")

        # La date du tournoi est un entier au format AAAAMMJJ (ex: 20240101)
        date_str = str(int(row["tourney_date"]))
        date = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))

        return {
            "sport":               TENNIS,
            "participant_1":       joueur_gagnant,
            "participant_2":       joueur_perdant,
            "score_participant_1": 1,
            "score_participant_2": 0,
            "date_match":          date,
        }
