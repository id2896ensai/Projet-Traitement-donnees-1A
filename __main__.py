import pandas as pd
from src.Analysis.homemade.TeamFinder import TeamFinder
from src.Model.sport import Sport
from src.Model.team import Team
from src.Parsers.BasketballTeamLoader import BasketballTeamLoader
from src.Parsers.parse_csv import parse_players_csv

sport = Sport("basketball", "ballon", 10, "blabla", sport_en_equipe=True)
A = ["Atlanta Hawks", "Boston Celtics"]

teams = BasketballTeamLoader().load_teams
print(TeamFinder(teams, A))
