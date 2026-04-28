from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.Basketball.BasketballTeamAdapter import BasketballTeamAdapter
from src.Parsers.Adapters.Basketball.BasketballMatchAdapter import BasketballMatchAdapter


class BasketballMatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for Basketball.

    This loader:
      1. Loads teams from team_filepath using BasketballTeamAdapter.
      2. Builds a teams dict {id: Team}.
      3. Passes the dict to BasketballMatchAdapter.
      4. Delegates CSV reading and object creation to GenericMatchLoader.
    """

    def __init__(self, match_filepath: str, team_filepath: str) -> None:
        teams = GenericTeamLoader(team_filepath, BasketballTeamAdapter()).load_as_dict("id")
        adapter = BasketballMatchAdapter(teams)
        super().__init__(match_filepath, adapter)
