"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from typing import List

from attr import dataclass


@dataclass
class Room:
    name: str  # Label for the current game instance
    team_1_players: List[str]
    team_1_score: int
    team_1_icon: str
    team_2_players: List[str]
    team_2_score: int
    team_2_icon: str
