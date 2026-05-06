import datetime
import pandas as pd
from Model.sport import Sport

FOOTBALL = Sport("Football", "ballon", 22, "Sport collectif avec but", True)


class FootballMatchAdapter:
    """
    Convertit une ligne de football_european_leagues/match.csv en dict Match.

    Colonnes CSV : date, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal

    Requiert un dict d'equipes pre-charge {team_api_id (int): Team}.
    La date est au format "2008-08-17 00:00:00" — on ne garde que la partie date.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_dom = self.equipes.get(int(row["home_team_api_id"]))
        equipe_ext = self.equipes.get(int(row["away_team_api_id"]))

        if equipe_dom is None or equipe_ext is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        date_str = str(row["date"]).split(" ")[0]

        return {
            "sport":        FOOTBALL,
            "participants": [equipe_dom, equipe_ext],
            "scores":       {equipe_dom: int(row["home_team_goal"]), equipe_ext: int(row["away_team_goal"])},
            "date_match":   datetime.date.fromisoformat(date_str),
        }
