from src.Common.utils import print_timings

import pandas as pd


@print_timings
def parse_players_csv(filepath: str, sep: str = ";") -> list:
    players = parce_csv(filepath, sep)
    if len(players) < 0:
        raise Exception(
            "Oh non, la méthode parce_csv n'a pas été implémentée, "
            "vous allez devoir le faire vous-mêmes :("
        )
    return players["full_name"]


def parce_csv(filepath: str, sep: str = ";"):
    df = pd.read_csv(filepath, sep=sep)
    return df


if __name__ == "__main__":
    df = parce_csv()
    print(df)
