import datetime
import pandas as pd
from Model.player import Player
from Model.sport import Sport

CHESS = Sport("Chess", "strategie", 1, "Jeu d'echecs individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class ChessTeamAdapter:
    """
    Convertit une ligne de chess/player.csv en dict Team (sport individuel).

    Colonnes CSV : name, fide_id, birth_year, gender, federation, fide_title

    Le full_name (nom brut du CSV) correspond exactement aux valeurs dans
    les colonnes player_1 / player_2 du CSV de matchs (cle de lookup).
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        ChessTeamAdapter._counter += 1

        full_name = str(row["name"]).strip() if pd.notna(row.get("name")) else f"Joueur_{ChessTeamAdapter._counter}"
        # Format CSV : "NOM, Prenom" ou juste "NOM"
        parties = full_name.split(", ", 1)
        nom = parties[0]
        prenom = parties[1] if len(parties) == 2 else "X"

        fide_id = int(row["fide_id"]) if pd.notna(row.get("fide_id")) else ChessTeamAdapter._counter

        try:
            dob = datetime.date(int(row["birth_year"]), 1, 1)
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        sexe = None
        if pd.notna(row.get("gender")):
            g = str(row["gender"]).strip().lower()
            sexe = "M" if g == "male" else "F" if g == "female" else None

        joueur = Player(
            id=fide_id,
            nom=nom,
            prenom=prenom,
            date_de_naissance=dob,
            pseudo=full_name,
            pays_de_naissance=str(row["federation"]) if pd.notna(row.get("federation")) else None,
            sexe=sexe,
            poids=0.0,
            taille=0.0,
            role=str(row["fide_title"]) if pd.notna(row.get("fide_title")) else None,
            team=None,
            sport=CHESS,
        )

        return {
            "id":           fide_id,
            "sport":        CHESS,
            "players":      [joueur],
            "full_name":    full_name,
            "abbreviation": full_name[:5],
            "country":      str(row["federation"]) if pd.notna(row.get("federation")) else None,
        }
