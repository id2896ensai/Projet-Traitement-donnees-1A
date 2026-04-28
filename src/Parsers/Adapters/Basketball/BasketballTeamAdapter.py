import pandas as pd

from src.Model.sports_catalogue import BASKETBALL


class BasketballTeamAdapter:
    """Maps a basketball/team.csv row to a Team constructor dict.

    CSV columns used:
        id           -> id
        full_name    -> full_name
        abbreviation -> abbreviation
        nickname     -> nickname
        city         -> city
        state        -> state
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "full_name":    str(row["full_name"]),
            "sport":        BASKETBALL,
            "id":           int(row["id"]),
            "abbreviation": str(row["abbreviation"]),
            "nickname":     str(row["nickname"]),
            "city":         str(row["city"]),
            "state":        str(row["state"]),
        }
