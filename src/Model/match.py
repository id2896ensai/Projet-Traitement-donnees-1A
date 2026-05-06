from datetime import date
from .sport import Sport


class Match:
    """
    Classe modélisant une rencontre sportive.

    Cette classe est volontairement générique afin de pouvoir représenter :
    - des sports d'équipe (football, basket, volley...)
    - des sports individuels (course, natation...)
    - des compétitions à plusieurs participants.

    Attributes
    ----------
    sport : Sport
        Sport pratiqué lors de la rencontre.

    participants : list
        Liste des participants (équipes ou joueurs).

    scores : dict
        Dictionnaire associant chaque participant à son résultat.

        Exemples
        --------
        Football :
        {
            PSG: 3,
            OM: 1
        }

        Course :
        {
            Kipchoge: "2h01m09s",
            Bekele: "2h03m11s"
        }

    date_match : date
        Date de la rencontre.
    """

    def __init__(
        self,
        sport: Sport,
        participants: list,
        scores: dict,
        date_match: date,
    ):
        if not isinstance(sport, Sport):
            raise TypeError("sport doit être une instance de Sport")

        if not isinstance(participants, list):
            raise TypeError("participants doit être une liste")

        if len(participants) < 2:
            raise ValueError(
                "Il faut au moins deux participants"
            )

        if not isinstance(scores, dict):
            raise TypeError("scores doit être un dictionnaire")

        if not isinstance(date_match, date):
            raise TypeError(
                "date_match doit être une instance de date"
            )

        if date_match > date.today():
            raise ValueError(
                "La date du match ne peut pas être dans le futur"
            )

        for participant in participants:

            if not hasattr(participant, "sport"):
                raise ValueError(
                    "Chaque participant doit posséder un attribut 'sport'"
                )

            # Vérifie cohérence du sport
            if participant.sport != sport:
                raise ValueError(
                    "Tous les participants doivent pratiquer le sport du match"
                )

        for participant in participants:

            if participant not in scores:
                raise ValueError(
                    f"Le participant {participant} n'a pas de score associé"
                )

        self.sport = sport
        self.participants = participants
        self.scores = scores
        self.date_match = date_match

    def __str__(self) -> str:
        """
        Représentation lisible du match.
        """

        lignes = [
            f"Match [{self.sport.nom}]",
            f"Date : {self.date_match}",
            "Résultats :"
        ]

        for participant, score in self.scores.items():
            lignes.append(
                f"- {participant} : {score}"
            )

        return "\n".join(lignes)

    def __repr__(self) -> str:
        """
        Représentation technique du match.
        """

        return (
            f"Match("
            f"sport={repr(self.sport)}, "
            f"participants={repr(self.participants)}, "
            f"scores={repr(self.scores)}, "
            f"date_match={self.date_match}"
            f")"
        )
