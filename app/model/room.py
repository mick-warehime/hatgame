"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from enum import Enum
from itertools import chain
from typing import List, Iterable, Optional

from attr import dataclass

from app.model.player import Player


class GameModes(Enum):
    """Enumeration of game modes."""
    LOBBY = 'lobby'
    CLUE_GIVING_PRE = 'clue_giving_pre'
    CLUE_GIVING = 'clue_giving'
    TURN_RECAP = 'turn_recap'
    ROUND_RECAP = 'round_recap'


@dataclass
class Room:
    name: str  # Label for the current game instance
    team_1_players: List[Player]
    team_1_score: int
    team_1_icon: str
    team_2_players: List[Player]
    team_2_score: int
    team_2_icon: str
    game_mode: GameModes
    game_round: int
    clue_giver: Player
    last_clue_giver: Optional[Player]

    def all_players(self) -> Iterable[Player]:
        return chain(self.team_1_players, self.team_2_players)

    def all_phrases(self) -> List[str]:
        return [p for player in self.all_players() for p in player.phrases]
