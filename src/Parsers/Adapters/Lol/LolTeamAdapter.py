import pandas as pd

from src.Model.sports_catalogue import LOL


class LolTeamAdapter:
    """Maps a league_of_legends/team.csv row to a Team dict.

    CSV columns:
        team              -> full_name
        team_abbreviation -> abbreviation
        location          -> city
        region            -> region
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
