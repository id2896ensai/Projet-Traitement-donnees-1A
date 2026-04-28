import pandas as pd

from src.Model.sports_catalogue import STARCRAFT2


class Starcraft2PlayerAdapter:
    """Maps a starcraft_2/player.csv row to a Player dict.

    CSV columns:
        pseudo      -> id + pseudo
        name        -> prenom + nom  (format "Firstname Lastname")
        nationality -> pays_de_naissance
        birthdate   -> date_de_naissance  (format YYYY-MM-DD)
        race        -> role  ("Protoss", "Terran", "Zerg")
        team        -> (team name, stored as str)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
