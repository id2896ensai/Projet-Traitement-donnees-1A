import pandas as pd

from src.Model.sports_catalogue import CS2


class CS2MatchAdapter:
    """Maps a counter_strike_2/match.csv row to a Match dict.

    Requires a pre-loaded teams dict {team_name (str): Team}.

    CSV columns:
        date         -> date_match  (format YYYY-MM-DD)
        team_1       -> participant_1
        team_2       -> participant_2
        score_team_1 -> score_participant_1  (maps won)
        score_team_2 -> score_participant_2  (maps won)
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
