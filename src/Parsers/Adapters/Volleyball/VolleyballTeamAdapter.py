import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballTeamAdapter:
    """Maps a volleyball/country.csv row to a Team dict.

    In volleyball (JO 2024), teams are countries.

    CSV columns:
        code         -> id + abbreviation
        country_long -> full_name
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
