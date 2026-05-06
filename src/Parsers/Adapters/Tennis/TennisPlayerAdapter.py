import datetime
import pandas as pd
from Model.sport import Sport

TENNIS = Sport("Tennis", "raquette", 1, "Sport de raquette individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_dob(val) -> datetime.date:
    """Parse une date au format YYYYMMDD (entier ou float)."""
    try:
        s = str(int(float(val)))
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except (ValueError, TypeError):
        return _DATE_INCONNUE


class TennisPlayerAdapter:
    """
    Convertit une ligne de tennis/atp_players_2024.csv en dict Player.

    Colonnes CSV : player_id, name_first, name_last, hand, dob, ioc, height
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "id":                int(row["player_id"]),
            "nom":               str(row["name_last"]),
            "prenom":            str(row["name_first"]),
            "date_de_naissance": _parse_dob(row.get("dob")),
            "pseudo":            None,
            "pays_de_naissance": str(row["ioc"]) if pd.notna(row.get("ioc")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            float(row["height"]) if pd.notna(row.get("height")) else 0.0,
            "role":              None,
            "team":              None,
        }
