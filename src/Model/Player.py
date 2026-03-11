from typing import Union
from src.Common.utils import parse_boolean


class Player:
    """def __init__(self, id: int, full_name: str, is_the_goat: Union[str, bool]):
        self.id = id
        self.full_name = full_name
        self.is_the_goat = parse_boolean(is_the_goat)

    def __repr__(self):
        display_string = self.full_name
        if self.is_the_goat:
            display_string += " (GOAT)"
        return display_string
"""
    def __init__(self,id,nom,prenom,date_de_naissance,sexe,poids,taille):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.poids = poids
        self.taille = taille

    def __str__(self):
        return "Athlete : " + self.nom + " " + self.prenom
        + ", date de naissance : " + str(self.date_de_naissance)
        + ", sexe : " + self.sexe
        + ", poids : " + str(self.poids)
        + "taille : " + str(self.taille)
   
    def filtre_id(self,id_recherche):
        return id_recherche == self.id

    def filtre_nom(self,nom_recherche):
        return nom_recherche == self.nom

    def filtre_prenom(self, prenom_recherche):
        return prenom_recherche == self.prenom 
    
    def filtre_date_de_naissance(self, date_de_naissance):
        return date_de_naissance == self.date_de_naissance
    
    def filtre_sexe(self,sexe_recherche):
        return sexe_recherche == self.sexe
    
    def filtre_poids()