import pandas as pd
from Model.sport import Sport


BASKETBALL = Sport("Basketball", "ballon", 10, "Sport collectif avec panier", True)


class BasketballTeamAdapter:
    """
    Convertit une ligne de basketball/team.csv en dict prêt pour Team(**data).

    Colonnes CSV utilisées : id, full_name, abbreviation, nickname, city, state

    Pourquoi players=[] ?
    ---------------------
    Les joueurs sont chargés séparément. On initialise l'équipe sans joueurs,
    puis les matchs relient joueurs et équipes via team_id dans le CSV player.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "id":           int(row["id"]),
            "sport":        BASKETBALL,
            "players":      [],
            "full_name":    str(row["full_name"]),
            "abbreviation": str(row["abbreviation"]),
            "nickname":     str(row["nickname"]) if pd.notna(row.get("nickname")) else None,
            "city":         str(row["city"]) if pd.notna(row.get("city")) else None,
            "state":        str(row["state"]) if pd.notna(row.get("state")) else None,
        }
