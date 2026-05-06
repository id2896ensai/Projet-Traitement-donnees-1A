from src.Parsers.baseloader import BaseLoader
from src.Model.team import Team
from src.Model.player import Player
from src.Model.match import Match


class GenericTeamLoader(BaseLoader):
    """
    Loader générique pour charger des Team depuis n'importe quel CSV.
    Utilisé par tous les sports.

    Exemple
    -------
    teams = GenericTeamLoader(
        "data/basketball/team.csv",
        BasketballTeamAdapter()
    ).load_as_dict("id")
    """

    def create_object(self, data: dict) -> Team:
        return Team(**data)

    def load_as_dict(self, key_attr: str) -> dict:
        """
        Charge et indexe les équipes par un attribut.

        Parameters
        ----------
        key_attr : str
            Attribut utilisé comme clé du dict (ex: "id", "team_api_id")

        Returns
        -------
        dict[key_attr_value -> Team]
        """
        return {getattr(obj, key_attr): obj for obj in self.load()}


class GenericPlayerLoader(BaseLoader):
    """
    Loader générique pour charger des Player depuis n'importe quel CSV.
    Utilisé par tous les sports (équipe ou individuel).

    Exemple
    -------
    players = GenericPlayerLoader(
        "data/tennis/players.csv",
        TennisPlayerAdapter()
    ).load_as_dict("id")
    """

    def create_object(self, data: dict) -> Player:
        return Player(**data)

    def load_as_dict(self, key_attr: str) -> dict:
        """
        Charge et indexe les joueurs par un attribut.

        Parameters
        ----------
        key_attr : str
            Attribut utilisé comme clé (ex: "id")

        Returns
        -------
        dict[key_attr_value -> Player]
        """
        return {getattr(obj, key_attr): obj for obj in self.load()}


class GenericMatchLoader(BaseLoader):
    """
    Loader générique pour charger des Match depuis n'importe quel CSV.
    Universel pour tous les sports.

    Exemple
    -------
    # basket
    teams = GenericTeamLoader(...).load_as_dict("id")
    matches = GenericMatchLoader(
        "data/basketball/game.csv",
        BasketballMatchAdapter(teams=teams)
    ).load()

    # tennis
    players = GenericPlayerLoader(...).load_as_dict("id")
    matches = GenericMatchLoader(
        "data/tennis/matches.csv",
        TennisMatchAdapter(players=players)
    ).load()
    """

    def create_object(self, data: dict) -> Match:
        # Convertit le format plat (participant_1/2 + score_participant_1/2)
        # vers le format attendu par Match (participants + scores)
        if "participant_1" in data:
            p1 = data.pop("participant_1")
            p2 = data.pop("participant_2")
            s1 = data.pop("score_participant_1")
            s2 = data.pop("score_participant_2")
            data["participants"] = [p1, p2]
            data["scores"] = {p1: s1, p2: s2}
        return Match(**data)
