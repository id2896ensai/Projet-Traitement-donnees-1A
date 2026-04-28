from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.CS2.CS2TeamAdapter import CS2TeamAdapter
from src.Parsers.Adapters.CS2.CS2MatchAdapter import CS2MatchAdapter


class CS2MatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for Counter-Strike 2."""

    def __init__(self, match_filepath: str, team_filepath: str) -> None:
        teams = GenericTeamLoader(team_filepath, CS2TeamAdapter()).load_as_dict("full_name")
        adapter = CS2MatchAdapter(teams)
        super().__init__(match_filepath, adapter)
