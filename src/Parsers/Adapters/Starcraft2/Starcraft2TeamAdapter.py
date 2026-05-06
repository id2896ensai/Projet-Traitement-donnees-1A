import datetime
import pandas as pd
from Model.player import Player
from Model.sport import Sport

STARCRAFT2 = Sport("Starcraft2", "strategie", 1, "Jeu de strategie en temps reel individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class Starcraft2TeamAdapter:
    """
    Convertit une ligne de starcraft_2/player.csv en dict Team (sport individuel).

    Colonnes CSV : pseudo, name, nationality, birthdate, race, team

    L'equipe est indexee par full_name (= pseudo) pour etre retrouvee
    depuis les colonnes player_1 / player_2 du CSV de matchs.
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        Starcraft2TeamAdapter._counter += 1
        pseudo = str(row["pseudo"]).strip()
        nom_complet = str(row["name"]).strip() if pd.notna(row.get("name")) else ""
        parties = nom_complet.split(" ", 1)
        prenom = parties[0] if parties[0] else pseudo
        nom = parties[1] if len(parties) == 2 else "X"

        try:
            dob = datetime.date.fromisoformat(str(row["birthdate"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        joueur = Player(
            id=Starcraft2TeamAdapter._counter,
            nom=nom,
            prenom=prenom,
            date_de_naissance=dob,
            pseudo=pseudo,
            pays_de_naissance=str(row["nationality"]) if pd.notna(row.get("nationality")) else None,
            sexe=None,
            poids=0.0,
            taille=0.0,
            role=str(row["race"]) if pd.notna(row.get("race")) else None,
            team=None,
            sport=STARCRAFT2,
        )

        return {
            "id":           Starcraft2TeamAdapter._counter,
            "sport":        STARCRAFT2,
            "players":      [joueur],
            "full_name":    pseudo,
            "abbreviation": pseudo[:10],
            "country":      str(row["nationality"]) if pd.notna(row.get("nationality")) else None,
        }
