from src.Parsers.generic_loaders import GenericMatchLoader, GenericPlayerLoader
from src.Parsers.Adapters.Starcraft2.Starcraft2PlayerAdapter import Starcraft2PlayerAdapter
from src.Parsers.Adapters.Starcraft2.Starcraft2MatchAdapter import Starcraft2MatchAdapter


class Starcraft2MatchLoader(GenericMatchLoader):
    """Wires player loading and match mapping for Starcraft 2."""

    def __init__(self, match_filepath: str, player_filepath: str) -> None:
        players = GenericPlayerLoader(player_filepath, Starcraft2PlayerAdapter()).load_as_dict("pseudo")
        adapter = Starcraft2MatchAdapter(players)
        super().__init__(match_filepath, adapter)
