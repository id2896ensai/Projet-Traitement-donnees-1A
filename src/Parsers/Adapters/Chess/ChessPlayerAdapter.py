import datetime
import pandas as pd
from src.Model.sport import Sport

CHESS = Sport("Chess", "strategie", 2, "Jeu d'echecs", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class ChessPlayerAdapter:
    """
    Convertit une ligne de chess/player.csv en dict Player.

    Colonnes CSV : fide_id, name (format "Nom, Prenom"), birth_year, gender, federation, fide_title

    Le nom brut est stocké dans pseudo car c'est la clé utilisée dans match.csv
    pour retrouver le joueur (ChessMatchAdapter fait players.get(raw_name)).

    birth_year → on approxime à date(annee, 1, 1) car seule l'année est disponible.
    Person exige un objet date, pas None.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raw_name = str(row["name"]).strip()
        parts = raw_name.split(", ", 1)
        nom = parts[0]
        prenom = parts[1] if len(parts) == 2 else "Inconnu"

        birth_year = row.get("birth_year")
        try:
            dob = datetime.date(int(birth_year), 1, 1)
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        fide_id = row.get("fide_id")
        return {
            "id":                int(fide_id) if pd.notna(fide_id) else abs(hash(raw_name)) % (10**7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            raw_name,
            "pays_de_naissance": str(row["federation"]) if pd.notna(row.get("federation")) else None,
            "sexe":              str(row["gender"]) if pd.notna(row.get("gender")) else None,
            "poids":             0.0,
            "taille":            0.0,
            "role":              str(row["fide_title"]) if pd.notna(row.get("fide_title")) else None,
            "team":              None,
            "sport":             CHESS,
        }
