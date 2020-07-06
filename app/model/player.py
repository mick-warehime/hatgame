"""Data object representing a player.
"""
from typing import List, Iterable

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
