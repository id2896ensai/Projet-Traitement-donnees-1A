import datetime
import pandas as pd
from Model.sport import Sport

FOOTBALL_CL = Sport("Football Champions League", "ballon", 22, "Ligue des Champions UEFA", True)


class FootballCLMatchAdapter:
    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row) -> dict:
        equipe_dom = self.equipes.get(str(row["team_home"]).strip())
        equipe_ext = self.equipes.get(str(row["team_away"]).strip())
        if equipe_dom is None or equipe_ext is None:
            raise KeyError("Equipe introuvable")
        return {
            "sport":        FOOTBALL_CL,
            "participants": [equipe_dom, equipe_ext],
            "scores":       {equipe_dom: int(row["score_team_home"]), equipe_ext: int(row["score_team_away"])},
            "date_match":   datetime.date.fromisoformat(str(row["date"])),
        }
