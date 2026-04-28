from abc import ABC, abstractmethod

from src.Parsers.readers.csv_reader import read_csv


class BaseLoader(ABC):
    """Abstract base for all sport loaders.

    Subclasses only implement create_object(data).
    The CSV reading loop and adapter call are handled here.

    Args:
        filepath: Path to the CSV file.
        adapter:  Object with an adapt(row) method that returns a dict.
        sep:      CSV separator (default ",").
    """

    def __init__(self, filepath: str, adapter, sep: str = ",") -> None:
        self.filepath = filepath
        self.adapter = adapter
        self.sep = sep

    def load(self) -> list:
        """Read the CSV and return a list of model objects.

        Rows that fail adapt() or create_object() are silently skipped.

        Returns:
            list: Model objects built from the CSV rows.
        """
        df = read_csv(self.filepath, sep=self.sep)
        objects = []
        for _, row in df.iterrows():
            try:
                data = self.adapter.adapt(row)
                obj = self.create_object(data)
                objects.append(obj)
            except (ValueError, KeyError, TypeError):
                continue
        return objects

    @abstractmethod
    def create_object(self, data: dict):
        """Instantiate a model object from the normalised dict.

        Args:
            data: Dict produced by adapter.adapt(row).

        Returns:
            A model object (Player, Team, Match, …).
        """
