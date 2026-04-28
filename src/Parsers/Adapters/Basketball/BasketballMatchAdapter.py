import datetime

import pandas as pd

from src.Model.sports_catalogue import BASKETBALL


class BasketballMatchAdapter:
    """Maps a basketball/game.csv row to a Match constructor dict.

    Requires a pre-loaded teams dict to resolve team IDs.

    CSV columns used:
        game_date    -> date_match        (format YYYY-MM-DD)
        team_id_home -> participant_1     (looked up in teams dict)
        team_id_away -> participant_2     (looked up in teams dict)
        pts_home     -> score_participant_1
        pts_away     -> score_participant_2
    """

    def __init__(self, teams: dict) -> None:
        """Args:
            teams: {team_id (int): Team} — produced by GenericTeamLoader.load_as_dict("id").
        """
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        return {
            "sport":               BASKETBALL,
            "participant_1":       self.teams[int(row["team_id_home"])],
            "participant_2":       self.teams[int(row["team_id_away"])],
            "score_participant_1": int(row["pts_home"]),
            "score_participant_2": int(row["pts_away"]),
            "date_match":          datetime.date.fromisoformat(str(row["game_date"])),
        }
