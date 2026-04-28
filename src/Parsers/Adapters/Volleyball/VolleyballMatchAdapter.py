import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballMatchAdapter:
    """Maps a volleyball match CSV row to a Match dict.

    Requires a pre-loaded teams dict {country_code (str): Team}.

    CSV columns:
        date           -> date_match  (format YYYY-MM-DD)
        country_code_1 -> participant_1
        country_code_2 -> participant_2
        set_country_1  -> score_participant_1
        set_country_2  -> score_participant_2
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
