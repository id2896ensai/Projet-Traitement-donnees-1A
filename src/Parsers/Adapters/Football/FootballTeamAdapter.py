import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballTeamAdapter:
    """Maps a football_european_leagues/team.csv row to a Team dict.

    CSV columns:
        team_api_id    -> id
        team_long_name -> full_name
        team_short_name-> abbreviation
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
