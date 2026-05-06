import datetime
from Model.sport import Sport

CS2 = Sport("Counter-Strike 2", "esport", 10, "FPS tactique 5v5", True)


class CS2MatchAdapter:
    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row) -> dict:
        equipe_1 = self.equipes.get(str(row["team_1"]).strip())
        equipe_2 = self.equipes.get(str(row["team_2"]).strip())
        if equipe_1 is None or equipe_2 is None:
            raise KeyError("Equipe introuvable")
        return {
            "sport":        CS2,
            "participants": [equipe_1, equipe_2],
            "scores":       {equipe_1: int(row["score_team_1"]), equipe_2: int(row["score_team_2"])},
            "date_match":   datetime.date.fromisoformat(str(row["date"])),
        }
