import pandas as pd

from src.Model.sports_catalogue import LOL


class LolPlayerAdapter:
    """Maps a league_of_legends/player.csv row to a Player dict.

    CSV columns:
        pseudo           -> id + pseudo
        name             -> nom + prenom  (split "Firstname Lastname")
        country_of_birth -> pays_de_naissance
        birthdate        -> date_de_naissance  (format YYYY-MM-DD)
        role             -> role  ("top", "jungle", "mid", "bot", "sup")
        team             -> (team name, stored as str)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
