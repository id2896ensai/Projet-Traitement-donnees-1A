import pandas as pd

from src.Model.sports_catalogue import LOL


class LolMatchAdapter:
    """Maps a league_of_legends/match.csv row to a Match dict.

    Requires a pre-loaded teams dict {team_name (str): Team}.

    CSV columns:
        date       -> date_match  (format YYYY-MM-DD)
        team_blue  -> participant_1
        team_red   -> participant_2
        winner     -> determines score (winner=1, loser=0)

    Score convention: 1 (win) / 0 (loss) — no numeric score in LoL.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
