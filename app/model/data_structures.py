"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from functools import reduce
from itertools import chain
from typing import List, Iterable, Set

from attr import dataclass


@dataclass
class Player:
    """Represents a build_player in a game room"""
    name: str
    ready: bool
    phrases: List[str]


def build_player(name: str,
                 ready: bool = False,
                 phrases: Iterable[str] = ()) -> Player:
    """Builder function for Player objects"""
    return Player(name, ready, list(phrases))


@dataclass
class Room:
    name: str  # Label for the current game instance
    team_1_players: List[Player]
    team_1_score: int
    team_1_icon: str
    team_2_players: List[Player]
    team_2_score: int
    team_2_icon: str

    def all_players(self) -> Iterable[Player]:
        return chain(self.team_1_players, self.team_2_players)

    def all_phrases(self) -> Set[str]:
        return reduce(set.union, (set(p.phrases) for p in self.all_players()),
                      set())
