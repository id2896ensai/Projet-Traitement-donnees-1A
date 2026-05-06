import datetime
import pandas as pd
from src.Model.sport import Sport

LOL = Sport("LeagueOfLegends", "esport", 5, "Jeu de strategie en equipe 5v5", True)


class LolMatchAdapter:
    """
    Convertit une ligne de league_of_legends/match.csv en dict Match.

    Colonnes CSV : date, team_blue, team_red, winner, ...

    Requiert un dict d'equipes pre-charge {abbreviation (str): Team}.
    Score : equipe gagnante = 1, perdante = 0.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        abbrev_blue = str(row["team_blue"]).strip()
        abbrev_red = str(row["team_red"]).strip()

        team_blue = self.teams.get(abbrev_blue)
        team_red = self.teams.get(abbrev_red)

        if team_blue is None or team_red is None:
            raise KeyError(f"Equipe introuvable : '{abbrev_blue}' ou '{abbrev_red}'")

        winner = str(row["winner"]).strip()
        score_blue = 1 if winner == abbrev_blue else 0
        score_red = 1 if winner == abbrev_red else 0

        return {
            "sport":               LOL,
            "participant_1":       team_blue,
            "participant_2":       team_red,
            "score_participant_1": score_blue,
            "score_participant_2": score_red,
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
