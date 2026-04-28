from abc import ABC, abstractmethod
from typing import List

from src.Model.match import Match
from src.Model.player import Player
from src.Model.team import Team


class BasePlayerLoader(ABC):
    """Abstract base class for all sport-specific player loaders."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @abstractmethod
    def load_all_players(self) -> List[Player]:
        """Load all players from the CSV file.

        Returns:
            List[Player]: List of Player objects.
        """


class BaseTeamLoader(ABC):
    """Abstract base class for all sport-specific team loaders."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @abstractmethod
    def load_all_teams(self) -> List[Team]:
        """Load all teams from the CSV file.

        Returns:
            List[Team]: List of Team objects.
        """


class BaseMatchLoader(ABC):
    """Abstract base class for all sport-specific match loaders."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @abstractmethod
    def load_all_matches(self) -> List[Match]:
        """Load all matches from the CSV file.

        Returns:
            List[Match]: List of Match objects.
        """
