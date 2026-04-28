import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballMatchAdapter:
    """Maps a football_european_leagues/match.csv row to a Match dict.

    Requires a pre-loaded teams dict {team_api_id: Team}.

    CSV columns:
        date               -> date_match  (format "YYYY-MM-DD HH:MM:SS")
        home_team_api_id   -> participant_1
        away_team_api_id   -> participant_2
        home_team_goal     -> score_participant_1
        away_team_goal     -> score_participant_2

    Note: football allows draws (equal goals) -> get_winner() returns None.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
