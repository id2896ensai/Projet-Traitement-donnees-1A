import datetime

import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballMatchAdapter:
    """Convertit une ligne de football_european_leagues/match.csv en dict Match.

    Requiert un dictionnaire d'equipes pre-charge {team_api_id (int): Team}.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_dom = self.equipes.get(int(row["home_team_api_id"]))
        equipe_ext = self.equipes.get(int(row["away_team_api_id"]))

        if equipe_dom is None or equipe_ext is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        # La date est au format "2008-08-17 00:00:00" — on garde la partie date uniquement
        date_str = str(row["date"]).split(" ")[0]

        return {
            "sport":               FOOTBALL,
            "participant_1":       equipe_dom,
            "participant_2":       equipe_ext,
            "score_participant_1": int(row["home_team_goal"]),
            "score_participant_2": int(row["away_team_goal"]),
            "date_match":          datetime.date.fromisoformat(date_str),
        }
