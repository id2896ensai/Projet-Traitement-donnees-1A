from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.Football.FootballTeamAdapter import FootballTeamAdapter
from src.Parsers.Adapters.Football.FootballMatchAdapter import FootballMatchAdapter


class FootballMatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for Football (European leagues).

    Same pattern as BasketballMatchLoader — implement FootballTeamAdapter
    and FootballMatchAdapter first, then this class works automatically.
    """

    def __init__(self, match_filepath: str, team_filepath: str) -> None:
        teams = GenericTeamLoader(team_filepath, FootballTeamAdapter()).load_as_dict("id")
        adapter = FootballMatchAdapter(teams)
        super().__init__(match_filepath, adapter)
