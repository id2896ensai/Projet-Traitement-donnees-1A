from .player import Player
from .sport import Sport


class Team:
    """Classe modélisant une équipe"""

    def __init__(
        self,
        id: int,
        team_api_id: int | None,
        full_name: str,
        abbreviation: str,
        nickname: str | None,
        city: str | None,
        state: str | None,
        country: str | None,
        region: str | None,
        nb_players: int,
        players: list[Player],
        sport: Sport
    ) -> None:

        self.id = id
        self.team_api_id = team_api_id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.nickname = nickname
        self.city = city
        self.state = state
        self.country = country
        self.region = region
        self.nb_players = nb_players
        self.players = players
        self.sport = Sport

    def __str__(self):
        return "Id de la team : " + self.id + "/n"
        + "API ID de la team (si existante) : " + self.team_api_id + "/n"
        + "Nom complet de la team : " + self.full_name + "/n"
        + "Nom abrégé : " + self.abbreviation + "/n"
        + "Ville : " + self.city + "/n"
        + "Etat : " + self.state + "/n"
        + "Pays : " + self.country + "/n"
        + "Region du monde : " + self.region + "/n"
        + "Nombre de joueurs dans l'équipe : " + self.nb_players + "/n"
        + "Liste des joueurs de l'équipe : " + list[self.players] + "/n"
        + "Sport de l'équipe : " + self.sport + "/n"
