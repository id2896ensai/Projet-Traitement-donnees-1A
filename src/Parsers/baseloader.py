from abc import abstractmethod, ABC


class BaseLoader(ABC):
    """Classe abstraite des loaders de tous les sports"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

    @abstractmethod
    def load_data(self):
        pass
