class Sport:
    """Classe modélisant un sport"""

    def __init__(self, nom: str, categorie: str, nb_joueurs: int, description: str,
                 sport_en_equipe: bool):
        if not isinstance(nom, str):
            raise TypeError("Le nom doit être une str")
        if not nom.strip():
            raise ValueError("Le nom ne peut pas être vide")
        if not isinstance(categorie, str):
            raise TypeError("La catégorie doit être une str")
        if not isinstance(nb_joueurs, int):
            raise TypeError("Le nombre de joueurs doit être un int")
        if nb_joueurs < 1:
            raise ValueError("Le nombre de joueurs doit être >= 1")
        if not isinstance(description, str):
            raise TypeError("La description doit être une str")
        if not description.strip():
            raise ValueError("La description ne peut pas être vide")
        if not isinstance(sport_en_equipe, bool):
            raise TypeError("sport_en_equipe doit être un bool")
        self.nom = nom
        self.categorie = categorie
        self.nb_joueurs = nb_joueurs
        self.description = description
        self.sport_en_equipe = sport_en_equipe

    def __str__(self):
        type_sport = "collectif" if self.sport_en_equipe else "individuel"
        return (
            f"Sport : {self.nom}, catégorie : {self.categorie}, "
            f"nombre de joueurs nécessaire : {self.nb_joueurs}, "
            f"description : {self.description}, "
            f"Sport individuel ou collectif : {type_sport}"
        )

    def __repr__(self):
        return (
            f"Sport({self.nom}, categorie: {self.categorie}, "
            f"nb_joueurs: {self.nb_joueurs}, description: {self.description}, "
            f"sport_en_equipe: {self.sport_en_equipe})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sport):
            return NotImplemented
        return self.nom == other.nom

    def __hash__(self) -> int:
        return hash(self.nom)
