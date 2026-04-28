from src.Model.match import Match
from src.Model.player import Player
from src.Model.team import Team
from src.Parsers.baseloader import BaseLoader


class GenericPlayerLoader(BaseLoader):
    """Loader for any sport's players.

    Pass a sport-specific PlayerAdapter that defines adapt(row) -> dict.
    """

    def create_object(self, data: dict) -> Player:
        return Player(**data)

    def load_as_dict(self, key: str) -> dict:
        return {getattr(p, key): p for p in self.load()}


class GenericTeamLoader(BaseLoader):
    """Loader for any sport's teams.

    Pass a sport-specific TeamAdapter that defines adapt(row) -> dict.
    """

    def create_object(self, data: dict) -> Team:
        return Team(**data)

    def load_as_dict(self, key: str) -> dict:
        """Load teams and index them by one of their attributes.

        Args:
            key: Attribute name to use as dict key, e.g. "id" or "full_name".

        Returns:
            dict: {team.<key>: Team}
        """
        return {getattr(t, key): t for t in self.load()}


class GenericMatchLoader(BaseLoader):
    """Loader for any sport's matches.

    Pass a sport-specific MatchAdapter that defines adapt(row) -> dict.
    For sports where matches reference teams/players, the adapter receives
    those objects in its __init__ (see BasketballMatchAdapter for example).
    """

    def create_object(self, data: dict) -> Match:
        return Match(**data)
