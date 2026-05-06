import datetime
import pandas as pd
from src.Model.sport import Sport
from src.Model.team import Team

CHESS = Sport("Chess", "strategie", 2, "Jeu d'echecs", False)

_PLACEHOLDER_DATE = datetime.date(2024, 1, 1)


class ChessMatchAdapter:
    """
    Convertit une ligne de chess/match.csv en dict Match.

    Colonnes CSV : player_1, player_2, score_player_1, score_player_2

    Sport individuel → chaque joueur est wrappé dans une Team solo.
    Score : multiplié par 2 pour éviter les floats (0.5 → 1, 1.0 → 2).
    Les lignes avec adversaire "Bye" ou vide sont ignorées (raise ValueError).

    Requiert un dict de joueurs pré-chargé {pseudo/raw_name (str): Player}.
    """

    _counter = 0

    def __init__(self, players: dict) -> None:
        self.players = players

    def _solo_team(self, joueur) -> Team:
        """Crée une Team composée d'un seul joueur (sport individuel)."""
        ChessMatchAdapter._counter += 1
        return Team(
            id=ChessMatchAdapter._counter,
            sport=CHESS,
            players=[joueur],
            full_name=joueur.pseudo or f"{joueur.prenom} {joueur.nom}",
            abbreviation=(joueur.pseudo or joueur.nom)[:10],
        )

    def adapt(self, row: pd.Series) -> dict:
        p2_raw = row.get("player_2")
        if pd.isna(p2_raw) or str(p2_raw).strip().lower() in ("", "bye"):
            raise ValueError("Adversaire absent (Bye ou vide) — ligne ignorée")

        p1_name = str(row["player_1"]).strip()
        p2_name = str(p2_raw).strip()

        joueur_1 = self.players.get(p1_name)
        joueur_2 = self.players.get(p2_name)

        if joueur_1 is None or joueur_2 is None:
            raise KeyError(f"Joueur introuvable : '{p1_name}' ou '{p2_name}'")

        score_1 = int(float(row["score_player_1"]) * 2)
        score_2 = int(float(row["score_player_2"]) * 2)

        return {
            "sport":               CHESS,
            "participant_1":       self._solo_team(joueur_1),
            "participant_2":       self._solo_team(joueur_2),
            "score_participant_1": score_1,
            "score_participant_2": score_2,
            "date_match":          _PLACEHOLDER_DATE,
        }
