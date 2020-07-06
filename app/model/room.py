"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from itertools import chain
from typing import List, Iterable

from attr import dataclass

from app.model.player import Player


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

    def all_phrases(self) -> List[str]:
        return [p for player in self.all_players() for p in player.phrases]
