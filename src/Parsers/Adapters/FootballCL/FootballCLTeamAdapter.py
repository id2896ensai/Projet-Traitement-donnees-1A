import pandas as pd
from src.Model.sport import Sport

FOOTBALL_CL = Sport("Football Champions League", "ballon", 22, "Ligue des Champions UEFA", True)


class FootballCLTeamAdapter:
    """
    Convertit une ligne de football_champions_league/team.csv en dict Team.

    Colonnes CSV : full_name, short_name, country, city

    Pourquoi full_name=short_name ?
    --------------------------------
    Dans le CSV des matchs, les équipes sont référencées par short_name
    (ex: "Manchester City"). On utilise donc short_name comme full_name
    pour que load_as_dict("full_name") permette une lookup directe.
    Le vrai nom complet est mis dans nickname.
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        FootballCLTeamAdapter._counter += 1
        return {
            "id":           FootballCLTeamAdapter._counter,
            "sport":        FOOTBALL_CL,
            "players":      [],
            "full_name":    str(row["short_name"]),
            "abbreviation": str(row["short_name"])[:5],
            "nickname":     str(row["full_name"]) if pd.notna(row.get("full_name")) else None,
            "country":      str(row["country"]) if pd.notna(row.get("country")) else None,
            "city":         str(row["city"]) if pd.notna(row.get("city")) else None,
        }
