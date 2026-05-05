import datetime

import pandas as pd

from src.Model.sports_catalogue import STARCRAFT2


class Starcraft2PlayerAdapter:
    """Convertit une ligne de starcraft_2/player.csv en dict Player."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # Separation du vrai nom sur le premier espace
        nom_complet = str(row["name"]).strip()
        parties = nom_complet.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else ""

        naissance = row.get("birthdate")
        dob = datetime.date.fromisoformat(str(naissance)) if pd.notna(naissance) else None

        return {
            # Le pseudo est utilise comme cle de recherche dans le CSV des matchs
            "pseudo":            str(row["pseudo"]),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pays_de_naissance": str(row["nationality"]) if pd.notna(row.get("nationality")) else None,
            "role":              str(row["race"]) if pd.notna(row.get("race")) else None,
            "sport":             STARCRAFT2,
        }
