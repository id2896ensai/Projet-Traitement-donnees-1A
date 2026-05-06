import datetime
import pandas as pd
from src.Model.sport import Sport

BADMINTON = Sport("Badminton", "raquette", 2, "Sport de raquette individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class BadmintonPlayerAdapter:
    """
    Convertit une ligne de badminton/player.csv en dict Player.

    Pourquoi nom="Inconnu" et prenom depuis pseudo ?
    -------------------------------------------------
    Les CSVs badminton ne donnent souvent qu'un nom complet en une colonne.
    On stocke ce nom dans pseudo (identifiant de lookup dans les matchs)
    et on décompose sur le premier espace pour nom/prenom.
    Player exige nom et prenom non vides — "Inconnu" est le fallback.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        pseudo = str(row["name"]).strip()
        parties = pseudo.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        return {
            "id":                abs(hash(pseudo)) % (10**7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": _DATE_INCONNUE,
            "pseudo":            pseudo,
            "pays_de_naissance": str(row["country"]) if pd.notna(row.get("country")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            0.0,
            "role":              None,
            "team":              None,
            "sport":             BADMINTON,
        }
