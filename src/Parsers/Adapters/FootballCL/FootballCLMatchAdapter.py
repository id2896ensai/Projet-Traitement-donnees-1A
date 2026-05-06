import datetime
import pandas as pd
from Model.sport import Sport

FOOTBALL_CL = Sport("Football Champions League", "ballon", 22, "Ligue des Champions UEFA", True)


class FootballCLMatchAdapter:
    """
    Convertit une ligne de football_champions_league/match.csv en dict Match.

    Colonnes CSV : date, team_home, team_away, score_team_home, score_team_away

    Requiert un dict d'équipes pré-chargé {full_name/short_name (str): Team}.
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
