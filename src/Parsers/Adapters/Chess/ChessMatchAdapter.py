import datetime

import pandas as pd

from src.Model.sports_catalogue import CHESS

_PLACEHOLDER_DATE = datetime.date(2024, 1, 1)


class ChessMatchAdapter:
    """Maps a chess/match.csv row to a Match dict.

    Chess is INDIVIDUAL: player_1 vs player_2.
    Requires a pre-loaded players dict {raw_name (str): Player}.

    CSV columns:
        player_1       -> participant_1
        player_2       -> participant_2  (empty or "Bye" -> row skipped)
        score_player_1 -> score_participant_1  (float *2 to get int)
        score_player_2 -> score_participant_2

    Scores are stored as int (0.5 -> 1, 1.0 -> 2) to stay compatible with
    Match which expects integer scores.
    """

    def __init__(self, players: dict) -> None:
        self.players = players

    def adapt(self, row: pd.Series) -> dict:
        p2_raw = row.get("player_2")
        if pd.isna(p2_raw) or str(p2_raw).strip().lower() in ("", "bye"):
            raise ValueError("No valid opponent (Bye or empty)")

        p1_name = str(row["player_1"]).strip()
        p2_name = str(p2_raw).strip()

        participant_1 = self.players.get(p1_name)
        participant_2 = self.players.get(p2_name)

        if participant_1 is None or participant_2 is None:
            raise KeyError(f"Player not found: '{p1_name}' or '{p2_name}'")

        score_1 = int(float(row["score_player_1"]) * 2)
        score_2 = int(float(row["score_player_2"]) * 2)

        return {
            "sport":               CHESS,
            "participant_1":       participant_1,
            "participant_2":       participant_2,
            "score_participant_1": score_1,
            "score_participant_2": score_2,
            "date_match":          _PLACEHOLDER_DATE,
        }
