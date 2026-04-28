from typing import List, Tuple

from src.Model.match import Match
from src.Model.participant import Participant


def compute_podium(matches: List[Match], top_n: int = 3) -> List[Tuple[Participant, int]]:
    """Rank participants by number of wins.

    Works for both team and individual sports — any Match with a clear winner
    (no draw) counts toward the winner's tally.

    Args:
        matches: List of Match objects for a given sport.
        top_n:   Number of top participants to return.

    Returns:
        List of (Participant, win_count) tuples, sorted by win_count descending.
    """
    wins: dict[Participant, int] = {}
    for match in matches:
        winner = match.get_winner()
        if winner is not None:
            wins[winner] = wins.get(winner, 0) + 1
    return sorted(wins.items(), key=lambda x: x[1], reverse=True)[:top_n]
