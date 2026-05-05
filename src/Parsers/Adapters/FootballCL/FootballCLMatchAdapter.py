import datetime

import pandas as pd

from src.Model.sports_catalogue import FOOTBALL_CL


class FootballCLMatchAdapter:
    """Convertit une ligne de football_champions_league/match.csv en dict Match.

    Requiert un dictionnaire d'equipes pre-charge {short_name (str): Team}.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_dom = self.equipes.get(str(row["team_home"]).strip())
        equipe_ext = self.equipes.get(str(row["team_away"]).strip())

        if equipe_dom is None or equipe_ext is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        return {
            "sport":               FOOTBALL_CL,
            "participant_1":       equipe_dom,
            "participant_2":       equipe_ext,
            "score_participant_1": int(row["score_team_home"]),
            "score_participant_2": int(row["score_team_away"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
