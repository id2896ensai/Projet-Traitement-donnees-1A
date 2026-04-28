import datetime

import pandas as pd

from src.Model.sports_catalogue import BASKETBALL


def _parse_date(val) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(str(val))
    except (ValueError, TypeError):
        return None


class BasketballPlayerAdapter:
    """Maps a basketball/player.csv row to a Player constructor dict.

    CSV columns used:
        person_id  -> id
        last_name  -> nom
        first_name -> prenom
        birthdate  -> date_de_naissance  (format YYYY-MM-DD)
        height     -> taille             (format "6-8", stored as str)
        weight     -> poids              (in pounds)
        position   -> role
        team_id    -> (ignored here — resolved via match data)
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "id":                 int(row["person_id"]),
            "nom":                str(row["last_name"]),
            "prenom":             str(row["first_name"]),
            "date_de_naissance":  _parse_date(row.get("birthdate")),
            "taille":             str(row["height"]) if pd.notna(row.get("height")) else None,
            "poids":              float(row["weight"]) if pd.notna(row.get("weight")) else None,
            "role":               str(row["position"]) if pd.notna(row.get("position")) else None,
            "sport":              BASKETBALL,
        }
