import pandas as pd

from src.Model.sports_catalogue import FOOTBALL_CL


class FootballCLMatchAdapter:
    """Maps a football_champions_league/match.csv row to a Match dict.

    Requires a pre-loaded teams dict {short_name (str): Team}.

    CSV columns:
        date            -> date_match  (format YYYY-MM-DD)
        team_home       -> participant_1  (short_name)
        team_away       -> participant_2  (short_name)
        score_team_home -> score_participant_1
        score_team_away -> score_participant_2
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
