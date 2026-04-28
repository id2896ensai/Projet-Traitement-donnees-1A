import pandas as pd

from src.Model.sports_catalogue import FOOTBALL_CL


class FootballCLTeamAdapter:
    """Maps a football_champions_league/team.csv row to a Team dict.

    CSV columns:
        short_name   -> full_name  (display name)
        full_name    -> (stored as nickname)
        country      -> country
        city         -> city
        year_founded -> (ignored)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
