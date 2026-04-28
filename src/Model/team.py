from __future__ import annotations
from typing import TYPE_CHECKING

from src.Model.participant import Participant
from src.Model.sport import Sport

if TYPE_CHECKING:
    from src.Model.player import Player


class Team(Participant):
    """A sports team — participant in collective-sport matches."""

    def __init__(
        self,
        full_name: str,
        sport: Sport,
        id: int | None = None,
        abbreviation: str | None = None,
        nickname: str | None = None,
        city: str | None = None,
        state: str | None = None,
        country: str | None = None,
        region: str | None = None,
        players: list | None = None,
    ) -> None:
        self.full_name = full_name
        self.sport = sport
        self.id = id
        self.abbreviation = abbreviation
        self.nickname = nickname
        self.city = city
        self.state = state
        self.country = country
        self.region = region
        self.players: list[Player] = players or []

    def __str__(self) -> str:
        return f"[{self.sport.nom}] {self.full_name}"

    def __repr__(self) -> str:
        return f"Team({self.full_name!r})"
