import pandas as pd
from src.Model.sport import Sport

FOOTBALL = Sport("Football", "ballon", 22, "Sport collectif avec but", True)


class FootballTeamAdapter:
    """
    Convertit une ligne de football_european_leagues/team.csv en dict Team.

    Colonnes CSV : id, team_api_id, team_long_name, team_short_name

    Pourquoi id=team_api_id ?
    -------------------------
    Dans le CSV des matchs, les équipes sont référencées par team_api_id.
    On utilise donc team_api_id comme clé d'identification principale (id)
    pour que load_as_dict("id") permette une lookup directe depuis le match.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "id":           int(row["team_api_id"]),
            "sport":        FOOTBALL,
            "players":      [],
            "full_name":    str(row["team_long_name"]),
            "abbreviation": str(row["team_short_name"]),
        }
