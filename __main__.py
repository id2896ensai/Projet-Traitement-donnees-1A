import pandas as pd
from src.Analysis.homemade.TeamFinder import TeamFinder
from src.Model.sport import Sport
from src.Model.team import Team
from src.Parsers.BasketballTeamLoader import BasketballTeamLoader
from src.Parsers.parse_csv import parse_players_csv
from src.Analysis.pandas.GoatFinder import find_the_goat_in_df
from src.Analysis.homemade.GoatFinder import find_the_goat

setting = input("Select a setting, 0=pandas-powered, 1=àlamain-powered\n")

if setting == "0":
    players_df = pd.read_csv("./data/players.csv")
else:
    players = parse_players_csv("./data/players.csv")

print("Select your journey through the data")
print("1 - I want to know who is the greatest football player of all time")
input("2 - Just kidding, there's only one option\n")

if setting == "0":
    the_goat = find_the_goat_in_df(players_df)
else:
    the_goat = find_the_goat(players)

sport = Sport("basketball", "ballon", 10, "blabla", sport_en_equipe=True)
A = ["Atlanta Hawks", "Boston Celtics"]

teams = BasketballTeamLoader().load_teams
print(TeamFinder(teams, A))
