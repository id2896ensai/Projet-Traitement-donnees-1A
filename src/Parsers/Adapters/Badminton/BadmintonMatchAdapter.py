import datetime
import pandas as pd
from src.Model.sport import Sport
from src.Model.team import Team

BADMINTON = Sport("Badminton", "raquette", 2, "Sport de raquette individuel", False)


def _jeux_gagnes(score_jeu) -> tuple:
    """Retourne (jeux_gagnés_j1, jeux_gagnés_j2) pour un score au format 'X-Y'."""
    if pd.isna(score_jeu) or str(score_jeu).strip() == "":
        return 0, 0
    parties = str(score_jeu).strip().split("-")
    if len(parties) != 2:
        return 0, 0
    try:
        s1, s2 = int(parties[0]), int(parties[1])
        if s1 > s2:
            return 1, 0
        if s2 > s1:
            return 0, 1
    except ValueError:
        pass
    return 0, 0


class BadmintonMatchAdapter:
    """
    Convertit une ligne de badminton/match.csv en dict Match.

    Pourquoi wrapper le Player dans une Team ?
    ------------------------------------------
    Match.__init__ vérifie que chaque participant possède un attribut `sport`
    ET que ce sport correspond à celui du match. Team a cet attribut, mais
    Player aussi (grâce au champ sport qu'on lui ajoute).
    On wrappe le joueur dans une Team d'un seul joueur pour rester cohérent
    avec les sports d'équipe : un "participant" est toujours une Team.

    Requiert un dict de joueurs pré-chargé {pseudo (str): Player}.
    Score = nombre de jeux gagnés sur les 3 manches possibles.
    """

    _counter = 0

    def __init__(self, joueurs: dict) -> None:
        self.joueurs = joueurs

    def _solo_team(self, joueur) -> Team:
        """Crée une Team composée d'un seul joueur (sport individuel)."""
        BadmintonMatchAdapter._counter += 1
        return Team(
            id=BadmintonMatchAdapter._counter,
            sport=BADMINTON,
            players=[joueur],
            full_name=joueur.pseudo or f"{joueur.prenom} {joueur.nom}",
            abbreviation=(joueur.pseudo or joueur.nom)[:10],
        )

    def adapt(self, row: pd.Series) -> dict:
        nom_j1 = str(row["player_1"]).strip()
        nom_j2 = str(row["player_2"]).strip()

        joueur_1 = self.joueurs.get(nom_j1)
        joueur_2 = self.joueurs.get(nom_j2)

        if joueur_1 is None or joueur_2 is None:
            raise KeyError(f"Joueur introuvable : '{nom_j1}' ou '{nom_j2}'")

        score_1, score_2 = 0, 0
        for col in ["game_1_score", "game_2_score", "game_3_score"]:
            v1, v2 = _jeux_gagnes(row.get(col))
            score_1 += v1
            score_2 += v2

        return {
            "sport":               BADMINTON,
            "participant_1":       self._solo_team(joueur_1),
            "participant_2":       self._solo_team(joueur_2),
            "score_participant_1": score_1,
            "score_participant_2": score_2,
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
