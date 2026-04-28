import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballPlayerAdapter:
    """Maps a football_european_leagues/player.csv row to a Player dict.

    CSV columns:
        player_api_id -> id
        player_name   -> nom + prenom  (split "Firstname Lastname")
        birthday      -> date_de_naissance  (format YYYY-MM-DD)
        weight (kg)   -> poids
        height (cm)   -> taille
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
