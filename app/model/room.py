"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Room:
    name: str  # Label for the current game instance
    team_1_players: Tuple[str, ...]
    team_1_score: int
    team_1_icon: str
    team_2_players: Tuple[str, ...]
    team_2_score: int
    team_2_icon: str
