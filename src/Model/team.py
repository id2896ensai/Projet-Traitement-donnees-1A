from .player import Player
from .sport import Sport


class Team:
    """Classe modélisant une équipe sportive.

    Attributes
    ----------
    id : int
        Identifiant unique de l'équipe en base de données.
    team_api_id : int or None
        Identifiant de l'équipe dans l'API externe, None si inexistant.
    full_name : str
        Nom complet de l'équipe.
    abbreviation : str
        Nom abrégé de l'équipe
    nickname : str or None
        Surnom de l'équipe, None si inexistant.
    city : str or None
        Ville de l'équipe, None si non renseignée.
    state : str or None
        État/région administrative de l'équipe, None si non renseigné.
    country : str or None
        Pays de l'équipe, None si non renseigné.
    region : str or None
        Région du monde de l'équipe, None si non renseignée.
    nb_players : int
        Nombre de joueurs dans l'équipe.
    players : list[Player]
        Liste des joueurs appartenant à l'équipe.
    sport : Sport
        Sport pratiqué par l'équipe.
    """

    def __init__(
        self,
        id: int,
        sport: Sport,
        players: list,
        team_api_id: int | None = None,
        full_name: str | None = None,
        abbreviation: str | None = None,
        nickname: str | None = None,
        city: str | None = None,
        state: str | None = None,
        country: str | None = None,
        region: str | None = None,
    ) -> None:

        if not isinstance(id, int):
            raise TypeError("id doit être un int")

        if not isinstance(sport, Sport):
            raise TypeError("sport doit être une instance de Sport")

        if not isinstance(players, list):
            raise TypeError("players doit être une liste")

        for p in players:
            if not isinstance(p, Player):
                raise TypeError("Chaque élément de players doit être un Player")

        if team_api_id is not None and not isinstance(team_api_id, int):
            raise TypeError("team_api_id doit être un int ou None")

        if full_name is not None and not isinstance(full_name, str):
            raise TypeError("full_name doit être une str ou None")

        if full_name is not None and not full_name.strip():
            raise ValueError("full_name ne peut pas être vide")

        if abbreviation is not None and not isinstance(abbreviation, str):
            raise TypeError("abbreviation doit être une str ou None")

        if nickname is not None and not isinstance(nickname, str):
            raise TypeError("nickname doit être une str ou None")

        if city is not None and not isinstance(city, str):
            raise TypeError("city doit être une str ou None")

        if state is not None and not isinstance(state, str):
            raise TypeError("state doit être une str ou None")

        if country is not None and not isinstance(country, str):
            raise TypeError("country doit être une str ou None")

        if region is not None and not isinstance(region, str):
            raise TypeError("region doit être une str ou None")
        self.id = id
        self.sport = sport
        self.players: list[Player] = players or []
        self.team_api_id = team_api_id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.nickname = nickname
        self.city = city
        self.state = state
        self.country = country
        self.region = region
        self.nb_players = len(self.players)

    def __str__(self):
        """Retourne une représentation lisible de l'équipe, destinée à l'affichage utilisateur.

        Returns
        -------
        str
            Chaîne de caractères décrivant les attributs de l'équipe de manière claire et lisible.
        """
        return (
            "Id de la team : "
            + str(self.id)
            + "\n"
            + "API ID de la team (si existante) : "
            + str(self.team_api_id)
            + "\n"
            + "Nom complet de la team : "
            + self.full_name
            + "\n"
            + "Nom abrégé : "
            + self.abbreviation
            + "\n"
            + "Surnom : "
            + str(self.nickname)
            + "\n"
            + "Ville : "
            + str(self.city)
            + "\n"
            + "Etat : "
            + str(self.state)
            + "\n"
            + "Pays : "
            + str(self.country)
            + "\n"
            + "Region du monde : "
            + str(self.region)
            + "\n"
            + "Nombre de joueurs dans l'équipe : "
            + str(self.nb_players)
            + "\n"
            + "Liste des joueurs de l'équipe : "
            + str(self.players)
            + "\n"
            + "Sport de l'équipe : "
            + str(self.sport)
            + "\n"
        )

    def __repr__(self):
        """Retourne une représentation technique de l'équipe, destinée au débogage.

        Returns
        -------
        str
            Chaîne de caractères contenant le nom de la classe et l'ensemble des attributs
            de l'instance.
        """
        return (
            "Team("
            + str(self.id)
            + ", team_api_id: "
            + str(self.team_api_id)
            + ", full_name: "
            + self.full_name
            + ", abbreviation: "
            + self.abbreviation
            + ", nickname: "
            + str(self.nickname)
            + ", city: "
            + str(self.city)
            + ", state: "
            + str(self.state)
            + ", country: "
            + str(self.country)
            + ", region: "
            + str(self.region)
            + ", nb_players: "
            + str(self.nb_players)
            + ", players: "
            + repr(self.players)
            + ", sport: "
            + repr(self.sport)
            + ")"
        )
