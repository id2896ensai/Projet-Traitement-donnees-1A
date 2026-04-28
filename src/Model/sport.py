class Sport:
    """Classe modélisant un sport"""

    def __init__(self, nom: str, categorie: str, nb_joueurs: int, description: str, sport_en_equipe: bool):
        self.nom = nom
        self.categorie = categorie
        self.nb_joueurs = nb_joueurs
        self.description = description
        self.sport_en_equipe = sport_en_equipe

    def __str__(self):
        if self.sport_en_equipe:
            texte = "collectif."
        elif not self.sport_en_equipe:
            texte = "individuel."
        return "Sport : " + self.nom
        + ", catégorie : " + str(self.categorie)
        + ", nombre de joueurs neccessaire : " + self.nb_joueurs
        + ", description : " + str(self.description)
        + ", Sport individuel ou collectif : " + texte
    
    def __repr__(self):
        return f"Sport({self.nom}, en_equipe={self.sport_en_equipe})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sport):
            return NotImplemented
        return self.nom == other.nom

    def __hash__(self) -> int:
        return hash(self.nom)