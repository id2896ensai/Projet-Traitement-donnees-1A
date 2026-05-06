from abc import ABC, abstractmethod


class BaseLoader(ABC):
    """
    Classe abstraite de base pour tous les loaders.
    """

    def __init__(self, filepath, adapter):

        self.filepath = filepath
        self.adapter = adapter

    def load(self):

        # sep=None + engine="python" laisse pandas détecter automatiquement
        import pandas as pd
        try:
            df = pd.read_csv(self.filepath, sep=None, engine="python")
        except FileNotFoundError:
            raise FileNotFoundError(f"Fichier introuvable : {self.filepath}")

        objects = []

        for _, row in df.iterrows():

            normalized_data = self.adapter.adapt(row)

            obj = self.create_object(normalized_data)

            objects.append(obj)

        return objects

    @abstractmethod
    def create_object(self, data: dict):
        """
        Crée un objet métier à partir des données normalisées.
        """
        pass
