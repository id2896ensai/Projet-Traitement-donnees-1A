import datetime

import pandas as pd

from src.Model.sports_catalogue import CS2


class CS2MatchAdapter:
    """Convertit une ligne de counter_strike_2/match.csv en dict Match.

    Requiert un dictionnaire d'equipes pre-charge {nom_equipe (str): Team}.
    Le score correspond au nombre de cartes (maps) gagnees.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_1 = self.equipes.get(str(row["team_1"]).strip())
        equipe_2 = self.equipes.get(str(row["team_2"]).strip())

        if equipe_1 is None or equipe_2 is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        return {
            "sport":               CS2,
            "participant_1":       equipe_1,
            "participant_2":       equipe_2,
            "score_participant_1": int(row["score_team_1"]),
            "score_participant_2": int(row["score_team_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
