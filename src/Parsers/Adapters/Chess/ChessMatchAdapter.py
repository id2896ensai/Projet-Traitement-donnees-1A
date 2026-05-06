import datetime
import pandas as pd
from Model.sport import Sport

CHESS = Sport("Chess", "strategie", 1, "Jeu d'echecs individuel", False)

_PLACEHOLDER_DATE = datetime.date(2024, 1, 1)


class ChessMatchAdapter:
    """
    Convertit une ligne de chess/match.csv en dict Match.

    Colonnes CSV : player_1, player_2, score_player_1, score_player_2

    Requiert un dict d'equipes pre-charge {full_name (str): Team}.
    Les Teams sont des equipes solo creees par ChessTeamAdapter.
    Score : multiplie par 2 pour eviter les floats (0.5 -> 1, 1.0 -> 2).
    Les lignes avec adversaire "Bye" ou vide sont ignorees.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        p2_raw = row.get("player_2")
        if pd.isna(p2_raw) or str(p2_raw).strip().lower() in ("", "bye"):
            raise ValueError("Adversaire absent (Bye ou vide) — ligne ignoree")

        p1_name = str(row["player_1"]).strip()
        p2_name = str(p2_raw).strip()

        team_1 = self.equipes.get(p1_name)
        team_2 = self.equipes.get(p2_name)

        if team_1 is None or team_2 is None:
            raise KeyError(f"Joueur introuvable : '{p1_name}' ou '{p2_name}'")

        score_1 = int(float(row["score_player_1"]) * 2)
        score_2 = int(float(row["score_player_2"]) * 2)

        return {
            "sport":        CHESS,
            "participants": [team_1, team_2],
            "scores":       {team_1: score_1, team_2: score_2},
            "date_match":   _PLACEHOLDER_DATE,
        }
