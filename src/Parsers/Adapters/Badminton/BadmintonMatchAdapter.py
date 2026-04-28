import pandas as pd

from src.Model.sports_catalogue import BADMINTON


class BadmintonMatchAdapter:
    """Maps a badminton/match.csv row to a Match dict.

    Badminton is INDIVIDUAL: player_1 vs player_2.
    Requires a pre-loaded players dict {player_name (str): Player}.

    CSV columns:
        date        -> date_match  (format YYYY-MM-DD)
        player_1    -> participant_1  (full name)
        player_2    -> participant_2  (full name)
        winner      -> determines score (winner=2, loser=1 or count games)
        game_1_score, game_2_score, game_3_score -> parse for game count
    """

    def __init__(self, players: dict) -> None:
        self.players = players

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
