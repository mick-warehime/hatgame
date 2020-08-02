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
    CLUE_GIVING = 'clue_giving'
    TURN_RECAP = 'turn_recap'
    ROUND_RECAP = 'round_recap'
    GAME_RECAP = 'game_recap'


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

    def update_player(self, name: str, new_player: Player) -> None:

        player_ind = None

        for team in (self.team_1_players, self.team_2_players):
            for ind, player in enumerate(team):
                if player.name == name:
                    player_ind = ind
                    break
            if player_ind is not None:
                team[player_ind] = new_player
                return
        assert player_ind is not None, f'Player {name} not found.'
