from baseloader import BaseLoader
import pandas as pd

class BasketLoader(BaseLoader):
    pass

    def __init__(self, filepath):
        super().__init__(filepath)

        self.files = {
            "players" : "player.csv",
            "games" : "game.csv",
            "teams" : "team.csv"
        }

    def load_data(self):
        for name,  file in self.files.items():
            path = self.filepath + "/" + file
            self.data[name] = pd.read_csv(path)
        return self.data