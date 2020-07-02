"""Implementation of data structures encoding current game state.

The implementation is hidden from app.py.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class GameState:
    name: str  # Label for the current game instance
    team_0_players: List[str]
    team_0_name: str
    team_0_score: int
    team_0_icon: str
    team_1_players: List[str]
    team_1_name: str
    team_1_score: int
    team_1_icon: str
