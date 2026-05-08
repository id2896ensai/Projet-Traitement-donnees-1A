import datetime
import pandas as pd
from Model.sport import Sport

BASKETBALL = Sport("Basketball", "ballon", 10, "Sport collectif avec panier", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_date(val: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(val)
    except ValueError:
        pass
    try:
        from dateutil import parser as du
        return du.parse(val).date()
    except Exception:
        return _DATE_INCONNUE


class BasketballMatchAdapter:

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:

        team1 = self.teams.get(int(row["team_id_home"]))
        team2 = self.teams.get(int(row["team_id_away"]))

        if team1 is None or team2 is None:
            raise ValueError("Team non trouvée")

        participants = [team1, team2]

        scores = {
            team1: int(row["pts_home"]),
            team2: int(row["pts_away"])
        }

        return {
            "sport": BASKETBALL,
            "participants": participants,
            "scores": scores,
            "date_match": _parse_date(str(row["game_date"]))
        }
