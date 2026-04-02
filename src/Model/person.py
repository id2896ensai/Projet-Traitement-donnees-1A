class Person:
    """ Classe modélisant une personne : joueur ou coach """
    def __init__(self, nom: str, prenom: str, date_de_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance