from __future__ import annotations
from typing import TYPE_CHECKING

from src.Model.participant import Participant
from src.Model.person import Person

if TYPE_CHECKING:
    from src.Model.sport import Sport
    from src.Model.team import Team


class Player(Person, Participant):
    """An individual athlete — participant in individual-sport matches,
    or member of a Team in collective-sport matches."""

    def __init__(
        self,
        nom: str = "",
        prenom: str = "",
        date_de_naissance=None,
        id=None,
        pseudo: str | None = None,
        pays_de_naissance: str | None = None,
        sexe: str | None = None,
        poids: float | None = None,
        taille: float | None = None,
        role: str | None = None,
        team: Team | None = None,
        sport: Sport | None = None,
    ) -> None:
        Person.__init__(self, nom=nom, prenom=prenom, date_de_naissance=date_de_naissance)
        self.id = id
        self.pseudo = pseudo
        self.pays_de_naissance = pays_de_naissance
        self.sexe = sexe
        self.poids = poids
        self.taille = taille
        self.role = role
        self.team = team
        self.sport = sport

    @property
    def full_name(self) -> str:
        """Return the best available display name."""
        if self.pseudo:
            return self.pseudo
        return f"{self.prenom} {self.nom}".strip()

    def __str__(self) -> str:
        sport_label = self.sport.nom if self.sport else "?"
        return f"[{sport_label}] {self.full_name}"

    def __repr__(self) -> str:
        return f"Player({self.full_name!r})"
