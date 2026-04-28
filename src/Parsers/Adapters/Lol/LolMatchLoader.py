from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.Lol.LolTeamAdapter import LolTeamAdapter
from src.Parsers.Adapters.Lol.LolMatchAdapter import LolMatchAdapter


class LolMatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for League of Legends."""

    def __init__(self, match_filepath: str, team_filepath: str) -> None:
        teams = GenericTeamLoader(team_filepath, LolTeamAdapter()).load_as_dict("full_name")
        adapter = LolMatchAdapter(teams)
        super().__init__(match_filepath, adapter)
