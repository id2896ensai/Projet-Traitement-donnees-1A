import datetime
import pandas as pd
from src.Model.sport import Sport
from src.Model.team import Team
from src.Model.player import Player

BADMINTON = Sport("Badminton", "raquette", 2, "Sport de raquette individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class BadmintonTeamAdapter:
    """
    Cree une Team d'un seul joueur depuis badminton/player.csv (sport individuel).

    Colonnes CSV : name, country

    Le pseudo (nom complet) est utilise comme full_name pour retrouver
    l'equipe dans le dictionnaire lors du chargement des matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        pseudo = str(row["name"]).strip()
        parties = pseudo.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        joueur = Player(
            id=abs(hash(pseudo)) % (10 ** 7),
            nom=nom,
            prenom=prenom,
            date_de_naissance=_DATE_INCONNUE,
            pseudo=pseudo,
            pays_de_naissance=str(row["country"]) if pd.notna(row.get("country")) else None,
            sexe=None,
            poids=0.0,
            taille=0.0,
            role=None,
            team=None,
            sport=BADMINTON,
        )

        return {
            "id":           abs(hash(pseudo)) % (10 ** 7),
            "sport":        BADMINTON,
            "players":      [joueur],
            "full_name":    pseudo,
            "abbreviation": pseudo[:10],
        }
