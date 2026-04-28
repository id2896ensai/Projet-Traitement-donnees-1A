import pandas as pd

from src.Model.sports_catalogue import CS2


class CS2PlayerAdapter:
    """Maps a counter_strike_2/player.csv row to a Player dict.

    CSV columns:
        pseudo      -> id + pseudo
        name        -> prenom + nom
        nationality -> pays_de_naissance
        birthdate   -> date_de_naissance  (format YYYY-MM-DD)
        role        -> role  ("rifler", "AWPer", "IGL", ...)
        team        -> (team name, stored as str)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
