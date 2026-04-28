import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballPlayerAdapter:
    """Maps a volleyball player CSV row to a Player dict.

    Works for player_men.csv and player_women.csv.

    CSV columns:
        name         -> nom + prenom  (format "LASTNAME Firstname")
        country_code -> pays_de_naissance
        height       -> taille  (in cm)
        birth_date   -> date_de_naissance  (format YYYY-MM-DD)

    Tip: names are uppercase "FROMM Christian" — split on first space.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
