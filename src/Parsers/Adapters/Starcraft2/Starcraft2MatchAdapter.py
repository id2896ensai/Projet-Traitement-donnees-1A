import pandas as pd

from src.Model.sports_catalogue import STARCRAFT2


class Starcraft2MatchAdapter:
    """Maps a starcraft_2/match.csv row to a Match dict.

    Starcraft 2 is INDIVIDUAL: player_1 vs player_2 by pseudo.
    Requires a pre-loaded players dict {pseudo (str): Player}.

    CSV columns:
        date           -> date_match  (format YYYY-MM-DD)
        player_1       -> participant_1  (pseudo)
        player_2       -> participant_2  (pseudo)
        score_player_1 -> score_participant_1  (maps won)
        score_player_2 -> score_participant_2  (maps won)
    """

    def __init__(self, players: dict) -> None:
        self.players = players

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
