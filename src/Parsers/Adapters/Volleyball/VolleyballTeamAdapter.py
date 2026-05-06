import pandas as pd
from Model.sport import Sport

VOLLEYBALL = Sport("Volleyball", "ballon", 6, "Sport collectif avec filet", True)


class VolleyballTeamAdapter:
    """
    Convertit une ligne de volleyball/country.csv en dict Team.

    Colonnes CSV : code, country, country_long

    L'equipe est indexee par abbreviation (code pays ex: "USA")
    pour etre retrouvee depuis les colonnes country_code_1/2 du CSV de matchs.
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        VolleyballTeamAdapter._counter += 1
        code = str(row["code"]).strip()
        return {
            "id":           VolleyballTeamAdapter._counter,
            "sport":        VOLLEYBALL,
            "players":      [],
            "full_name":    str(row["country_long"]),
            "abbreviation": code,
            "country":      str(row["country_long"]),
        }
