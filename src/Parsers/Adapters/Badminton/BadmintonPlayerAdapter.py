import pandas as pd

from src.Model.sports_catalogue import BADMINTON


class BadmintonPlayerAdapter:
    """Maps a badminton/player.csv row to a Player dict.

    CSV columns:
        name      -> prenom + nom  (format "Firstname Lastname")
        country   -> pays_de_naissance
        continent -> (ignored)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
