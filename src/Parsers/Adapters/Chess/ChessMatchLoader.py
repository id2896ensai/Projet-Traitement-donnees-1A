from src.Parsers.generic_loaders import GenericMatchLoader, GenericPlayerLoader
from src.Parsers.Adapters.Chess.ChessPlayerAdapter import ChessPlayerAdapter
from src.Parsers.Adapters.Chess.ChessMatchAdapter import ChessMatchAdapter


class ChessMatchLoader(GenericMatchLoader):
    """Wires player loading and match mapping for Chess."""

    def __init__(self, match_filepath: str, player_filepath: str) -> None:
        players = GenericPlayerLoader(player_filepath, ChessPlayerAdapter()).load_as_dict("full_name")
        adapter = ChessMatchAdapter(players)
        super().__init__(match_filepath, adapter)
