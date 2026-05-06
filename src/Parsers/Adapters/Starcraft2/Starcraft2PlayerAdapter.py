import datetime
import pandas as pd
from src.Model.sport import Sport

STARCRAFT2 = Sport("Starcraft2", "strategie", 1, "Jeu de strategie en temps reel individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class Starcraft2PlayerAdapter:
    """
    Convertit une ligne de starcraft_2/player.csv en dict Player.

    Colonnes CSV : pseudo, name, nationality, birthdate, race, team

    Le pseudo est utilise comme identifiant de lookup dans les matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        pseudo = str(row["pseudo"]).strip()
        nom_complet = str(row["name"]).strip() if pd.notna(row.get("name")) else ""
        parties = nom_complet.split(" ", 1)
        prenom = parties[0] if parties[0] else pseudo
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        try:
            dob = datetime.date.fromisoformat(str(row["birthdate"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        return {
            "id":                abs(hash(pseudo)) % (10 ** 7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            pseudo,
            "pays_de_naissance": str(row["nationality"]) if pd.notna(row.get("nationality")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            0.0,
            "role":              str(row["race"]) if pd.notna(row.get("race")) else None,
            "team":              None,
            "sport":             STARCRAFT2,
        }
