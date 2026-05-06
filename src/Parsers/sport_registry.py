# Registre centralisé : associe chaque sport aux adaptateurs,
# chemins CSV et paramètres de chargement.

from Parsers.Adapters.Basketball.BasketballTeamAdapter import BasketballTeamAdapter
from Parsers.Adapters.Basketball.BasketballPlayerAdapter import BasketballPlayerAdapter
from Parsers.Adapters.Basketball.BasketballMatchAdapter import BasketballMatchAdapter

from Parsers.Adapters.Badminton.BadmintonTeamAdapter import BadmintonTeamAdapter
from Parsers.Adapters.Badminton.BadmintonPlayerAdapter import BadmintonPlayerAdapter
from Parsers.Adapters.Badminton.BadmintonMatchAdapter import BadmintonMatchAdapter

from Parsers.Adapters.Chess.ChessTeamAdapter import ChessTeamAdapter
from Parsers.Adapters.Chess.ChessPlayerAdapter import ChessPlayerAdapter
from Parsers.Adapters.Chess.ChessMatchAdapter import ChessMatchAdapter

from Parsers.Adapters.Tennis.TennisTeamAdapter import TennisTeamAdapter
from Parsers.Adapters.Tennis.TennisPlayerAdapter import TennisPlayerAdapter
from Parsers.Adapters.Tennis.TennisMatchAdapter import TennisMatchAdapter

from Parsers.Adapters.Volleyball.VolleyballTeamAdapter import VolleyballTeamAdapter
from Parsers.Adapters.Volleyball.VolleyballPlayerAdapter import VolleyballPlayerAdapter
from Parsers.Adapters.Volleyball.VolleyballMatchAdapter import VolleyballMatchAdapter

from Parsers.Adapters.Starcraft2.Starcraft2TeamAdapter import Starcraft2TeamAdapter
from Parsers.Adapters.Starcraft2.Starcraft2PlayerAdapter import Starcraft2PlayerAdapter
from Parsers.Adapters.Starcraft2.Starcraft2MatchAdapter import Starcraft2MatchAdapter

from Parsers.Adapters.Lol.LolTeamAdapter import LolTeamAdapter
from Parsers.Adapters.Lol.LolPlayerAdapter import LolPlayerAdapter
from Parsers.Adapters.Lol.LolMatchAdapter import LolMatchAdapter

from Parsers.Adapters.Football.FootballTeamAdapter import FootballTeamAdapter
from Parsers.Adapters.Football.FootballPlayerAdapter import FootballPlayerAdapter
from Parsers.Adapters.Football.FootballMatchAdapter import FootballMatchAdapter

from Parsers.Adapters.FootballCL.FootballCLTeamAdapter import FootballCLTeamAdapter
from Parsers.Adapters.FootballCL.FootballCLMatchAdapter import FootballCLMatchAdapter

from Parsers.Adapters.CS2.CS2TeamAdapter import CS2TeamAdapter
from Parsers.Adapters.CS2.CS2PlayerAdapter import CS2PlayerAdapter
from Parsers.Adapters.CS2.CS2MatchAdapter import CS2MatchAdapter

# Chaque entrée contient :
#   team_csv / player_csv / match_csv  : chemins relatifs depuis src/
#   TeamAdapter / PlayerAdapter / MatchAdapter : classes d'adaptateurs
#   match_kwarg  : nom du paramètre de l'équipe dans MatchAdapter.__init__
#   team_key     : attribut utilisé pour indexer les équipes (load_as_dict)
#   sport_en_equipe : True = stats collectifs disponibles
SPORTS_REGISTRY = {
    "Basketball": {
        "team_csv":        "../data/basketball/team.csv",
        "player_csv":      "../data/basketball/player.csv",
        "match_csv":       "../data/basketball/game.csv",
        "TeamAdapter":     BasketballTeamAdapter,
        "PlayerAdapter":   BasketballPlayerAdapter,
        "MatchAdapter":    BasketballMatchAdapter,
        "match_kwarg":     "teams",
        "team_key":        "id",
        "sport_en_equipe": True,
    },
    "Badminton": {
        "team_csv":        "../data/badminton/player.csv",
        "player_csv":      "../data/badminton/player.csv",
        "match_csv":       "../data/badminton/match.csv",
        "TeamAdapter":     BadmintonTeamAdapter,
        "PlayerAdapter":   BadmintonPlayerAdapter,
        "MatchAdapter":    BadmintonMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "full_name",
        "sport_en_equipe": False,
    },
    "Echecs": {
        "team_csv":        "../data/chess/player.csv",
        "player_csv":      "../data/chess/player.csv",
        "match_csv":       "../data/chess/match.csv",
        "TeamAdapter":     ChessTeamAdapter,
        "PlayerAdapter":   ChessPlayerAdapter,
        "MatchAdapter":    ChessMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "full_name",
        "sport_en_equipe": False,
    },
    "Tennis": {
        "team_csv":        "../data/tennis/atp_players_2024.csv",
        "player_csv":      "../data/tennis/atp_players_2024.csv",
        "match_csv":       "../data/tennis/atp_matches_2024.csv",
        "TeamAdapter":     TennisTeamAdapter,
        "PlayerAdapter":   TennisPlayerAdapter,
        "MatchAdapter":    TennisMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "id",
        "sport_en_equipe": False,
    },
    "Volleyball": {
        "team_csv":        "../data/volleyball/country.csv",
        "player_csv":      "../data/volleyball/player_men.csv",
        "match_csv":       "../data/volleyball/match_men.csv",
        "TeamAdapter":     VolleyballTeamAdapter,
        "PlayerAdapter":   VolleyballPlayerAdapter,
        "MatchAdapter":    VolleyballMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "abbreviation",
        "sport_en_equipe": True,
    },
    "Starcraft 2": {
        "team_csv":        "../data/starcraft_2/player.csv",
        "player_csv":      "../data/starcraft_2/player.csv",
        "match_csv":       "../data/starcraft_2/match.csv",
        "TeamAdapter":     Starcraft2TeamAdapter,
        "PlayerAdapter":   Starcraft2PlayerAdapter,
        "MatchAdapter":    Starcraft2MatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "full_name",
        "sport_en_equipe": False,
    },
    "League of Legends": {
        "team_csv":        "../data/league_of_legends/team.csv",
        "player_csv":      "../data/league_of_legends/player.csv",
        "match_csv":       "../data/league_of_legends/match.csv",
        "TeamAdapter":     LolTeamAdapter,
        "PlayerAdapter":   LolPlayerAdapter,
        "MatchAdapter":    LolMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "abbreviation",
        "sport_en_equipe": True,
    },
    "Football (Ligues europeennes)": {
        "team_csv":        "../data/football_european_leagues/team.csv",
        "player_csv":      "../data/football_european_leagues/player.csv",
        "match_csv":       "../data/football_european_leagues/match.csv",
        "TeamAdapter":     FootballTeamAdapter,
        "PlayerAdapter":   FootballPlayerAdapter,
        "MatchAdapter":    FootballMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "id",
        "sport_en_equipe": True,
    },
    "Football (Champions League)": {
        "team_csv":        "../data/football_champions_league/team.csv",
        "player_csv":      None,
        "match_csv":       "../data/football_champions_league/match.csv",
        "TeamAdapter":     FootballCLTeamAdapter,
        "PlayerAdapter":   None,
        "MatchAdapter":    FootballCLMatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "full_name",
        "sport_en_equipe": True,
    },
    "CS2": {
        "team_csv":        "../data/counter_strike_2/team.csv",
        "player_csv":      "../data/counter_strike_2/player.csv",
        "match_csv":       "../data/counter_strike_2/match.csv",
        "TeamAdapter":     CS2TeamAdapter,
        "PlayerAdapter":   CS2PlayerAdapter,
        "MatchAdapter":    CS2MatchAdapter,
        "match_kwarg":     "equipes",
        "team_key":        "full_name",
        "sport_en_equipe": True,
    },
}
