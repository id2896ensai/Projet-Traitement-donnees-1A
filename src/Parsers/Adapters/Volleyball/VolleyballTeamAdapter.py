import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballTeamAdapter:
    """Convertit une ligne de volleyball/country.csv en dict Team.

    En volleyball (JO 2024), les equipes sont des pays.
    Le code pays (ex: "USA") est utilise comme cle dans le CSV des matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "full_name":    str(row["country_long"]),
            # Le code pays sert a retrouver l'equipe depuis le CSV des matchs
            "abbreviation": str(row["code"]),
            "sport":        VOLLEYBALL,
        }
