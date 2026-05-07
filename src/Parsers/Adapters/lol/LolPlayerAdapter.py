import datetime
import pandas as pd
from Model.sport import Sport

LOL = Sport("League of Legends", "esport", 10, "MOBA 5v5", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class LolPlayerAdapter:
    """
    Convertit une ligne de league_of_legends/player.csv en dict Player.

    Colonnes CSV : pseudo, name, country_of_birth, birthdate, role, team
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        nom_complet = str(row["name"]).strip() if pd.notna(row.get("name")) else ""
        parties = nom_complet.split(" ", 1)
        prenom = parties[0] if parties[0] else str(row["pseudo"])
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        try:
            dob = datetime.date.fromisoformat(str(row["birthdate"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        return {
            "id":                abs(hash(str(row["pseudo"]))) % (10 ** 7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            str(row["pseudo"]),
            "pays_de_naissance": str(row["country_of_birth"]) if pd.notna(row.get("country_of_birth")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            0.0,
            "role":              str(row["role"]) if pd.notna(row.get("role")) else None,
            "team":              None,
        }
