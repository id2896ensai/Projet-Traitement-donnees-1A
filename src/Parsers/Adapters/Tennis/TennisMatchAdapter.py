import pandas as pd

from src.Model.sports_catalogue import TENNIS


class TennisMatchAdapter:
    """Maps an ATP or WTA match CSV row to a Match dict.

    Tennis is an INDIVIDUAL sport: matches oppose two players.
    Requires a pre-loaded players dict {player_id (int): Player}.

    CSV columns:
        tourney_date -> date_match  (int YYYYMMDD, e.g. 20240101)
        winner_id    -> participant with score 1
        loser_id     -> participant with score 0

    Score convention: winner=1, loser=0.

    Tip:
        date = datetime.datetime.strptime(str(int(row["tourney_date"])), "%Y%m%d").date()
    """

    def __init__(self, players: dict) -> None:
        self.players = players

    def adapt(self, row: pd.Series) -> dict:
        raise NotImplementedError
