import datetime
import pandas as pd
from src.Model.sport import Sport

BASKETBALL = Sport("Basketball", "ballon", 10, "Sport collectif avec panier", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_date(val) -> datetime.date:
    """
    Tente de parser une date ISO. Retourne _DATE_INCONNUE si impossible.
    Person.__init__ exige un objet date (pas None), donc on ne peut pas
    mettre None même si la donnée est absente dans le CSV.
    """
    try:
        return datetime.date.fromisoformat(str(val))
    except (ValueError, TypeError):
        return _DATE_INCONNUE


class BasketballPlayerAdapter:
    """
    Convertit une ligne de basketball/player.csv en dict prêt pour Player(**data).

    Colonnes CSV : person_id, first_name, last_name, birthdate, height, weight, position

    Pourquoi poids/taille à 0.0 si absents ?
    -----------------------------------------
    Player.__init__ exige isinstance(poids, (int, float)) — None est refusé.
    On met 0.0 comme valeur sentinelle quand la donnée est manquante.

    Pourquoi team=None ?
    --------------------
    La relation joueur↔équipe est résolue via team_id dans le CSV, pas ici.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "id":                int(row["person_id"]),
            "nom":               str(row["last_name"]),
            "prenom":            str(row["first_name"]),
            "date_de_naissance": _parse_date(row.get("birthdate")),
            "pseudo":            None,
            "pays_de_naissance": None,
            "sexe":              None,
            "poids":             float(row["weight"]) if pd.notna(row.get("weight")) else 0.0,
            "taille":            float(row["height"].split("-")[0]) * 30.48 if pd.notna(row.get("height")) else 0.0,
            "role":              str(row["position"]) if pd.notna(row.get("position")) else None,
            "team":              None,
            "sport":             BASKETBALL,
        }
