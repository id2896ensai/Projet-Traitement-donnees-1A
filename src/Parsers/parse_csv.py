from src.Common.utils import print_timings

import pandas as pd
from pathlib import Path


@print_timings
def parse_players_csv(filepath: str, sep: str = ";") -> list:
    raise Exception(
        "Oh non, la méthode parce_csv n'a pas été implémentée, "
        "vous allez devoir le faire vous-mêmes :("
    )
    return list()



def read_players_csv():
    df = pd.read_csv("data/players.csv")
    return df


if __name__ == "__main__":
    df = read_players_csv()
    print(df)

