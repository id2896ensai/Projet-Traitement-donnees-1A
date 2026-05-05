import datetime

import pandas as pd

from src.Model.sports_catalogue import STARCRAFT2


class Starcraft2MatchAdapter:
    """Convertit une ligne de starcraft_2/match.csv en dict Match.

    Starcraft 2 est un sport individuel.
    Requiert un dictionnaire de joueurs pre-charge {pseudo (str): Player}.
    Le score correspond au nombre de cartes (maps) gagnees.
    """

    def __init__(self, joueurs: dict) -> None:
        self.joueurs = joueurs

    def adapt(self, row: pd.Series) -> dict:
        joueur_1 = self.joueurs.get(str(row["player_1"]).strip())
        joueur_2 = self.joueurs.get(str(row["player_2"]).strip())

        if joueur_1 is None or joueur_2 is None:
            raise KeyError("Joueur introuvable dans le dictionnaire")

        return {
            "sport":               STARCRAFT2,
            "participant_1":       joueur_1,
            "participant_2":       joueur_2,
            "score_participant_1": int(row["score_player_1"]),
            "score_participant_2": int(row["score_player_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
