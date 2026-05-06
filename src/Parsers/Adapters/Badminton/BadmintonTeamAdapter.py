import datetime
import pandas as pd
from Model.player import Player
from Model.sport import Sport

BADMINTON = Sport("Badminton", "volant", 1, "Sport individuel de raquette", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class BadmintonTeamAdapter:
    """
    Convertit une ligne de badminton/player.csv en dict Team (sport individuel).

    Colonnes CSV : name, country, continent

    Le full_name correspond exactement a la valeur dans les colonnes
    player_1 / player_2 du CSV de matchs (cle de lookup).
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        BadmintonTeamAdapter._counter += 1

        full_name = str(row["name"]).strip() if pd.notna(row.get("name")) else f"Joueur_{BadmintonTeamAdapter._counter}"
        parties = full_name.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "X"

        joueur = Player(
            id=BadmintonTeamAdapter._counter,
            nom=nom,
            prenom=prenom,
            date_de_naissance=_DATE_INCONNUE,
            pseudo=full_name,
            pays_de_naissance=str(row["country"]) if pd.notna(row.get("country")) else None,
            sexe=None,
            poids=0.0,
            taille=0.0,
            role=None,
            team=None,
            sport=BADMINTON,
        )

        return {
            "id":           BadmintonTeamAdapter._counter,
            "sport":        BADMINTON,
            "players":      [joueur],
            "full_name":    full_name,
            "abbreviation": full_name[:5],
            "country":      str(row["country"]) if pd.notna(row.get("country")) else None,
            "region":       str(row["continent"]) if pd.notna(row.get("continent")) else None,
        }
