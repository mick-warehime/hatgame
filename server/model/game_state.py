"""Implementation of data structures encoding current game state."""
import random
from dataclasses import dataclass
from typing import Tuple

from server.icons import ICONS


@dataclass
class GameState:
    name: str  # Label for the current game instance
    team_0_players: Tuple[str, ...]
    team_0_name: str
    team_0_score: int
    team_0_icon: str
    team_1_players: Tuple[str, ...]
    team_1_name: str
    team_1_score: int
    team_1_icon: str


def build_game(first_player: str, game_name: str,
               icons: Tuple[str, str] = None) -> GameState:
    """Construct an initial game data model.

    The game is populated by the first player, with team names set as default
    values.

    Args:
        first_player: Name of the first player.
        game_name: Name assigned to the game.
        icons: Icons desired for the two teams. If not specified they are chosen
            randomly.

    Returns:
        Data class storing current initial game state.
    """

    if icons is None:
        icons = random.sample(ICONS, 2)

    return GameState(game_name, (first_player,), 'Team 1', 0, icons[0], (),
                     'Team 2', 0, icons[1])
