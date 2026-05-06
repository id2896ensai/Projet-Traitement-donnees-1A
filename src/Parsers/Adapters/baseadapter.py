from abc import ABC, abstractmethod
import pandas as pd


class BaseAdapter(ABC):
    """
    Interface commune à tous les adapters.
    Un adapter traduit une ligne d'un dataframe en dict
    prêt à être passé au constructeur d'un objet métier.
    """

    @abstractmethod
    def adapt(self, row: pd.Series) -> dict:
        """
        Transforme une ligne CSV en dict de construction.

        Parameters
        ----------
        row : pd.Series
            Ligne brute issue de pd.read_csv()

        Returns
        -------
        dict
            Kwargs pour le constructeur de l'objet métier correspondant.
        """
        ...
