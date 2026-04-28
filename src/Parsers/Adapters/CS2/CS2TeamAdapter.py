import pandas as pd

from src.Model.sports_catalogue import CS2


class CS2TeamAdapter:
    """Maps a counter_strike_2/team.csv row to a Team dict.

    CSV columns:
        team              -> full_name
        team_abbreviation -> abbreviation
        location          -> country
        region            -> region
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
