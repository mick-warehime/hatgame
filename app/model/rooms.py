"""Logic for handling multiple game rooms."""
import random
from dataclasses import asdict
from typing import Dict, Any, Tuple

from app.icons import ICONS
from app.model.fields import GameFields
from app.model.game_state import GameState

_room_dict: Dict[str, GameState] = {}


def game_room_exists(room_name: str) -> bool:
    """Whether a game room with the given name already exists."""
    return room_name in _room_dict


def initialize_game_room(room_name: str,
                         first_player: str,
                         icons: Tuple[str, str] = None
                         ) -> None:
    """Initialize a game room with the desired properties.

    The game's name must not already exist in the database.
    The game is populated by the first player, with team names set as default
    values.

    Args:
        first_player: Name of the first player.
        room_name: Name assigned to the game.
        icons: Icons desired for the two teams. If not specified they are chosen
            randomly.
    """
    assert room_name not in _room_dict, (
        f'Tried to add ({room_name}) but a room with that name already '
        f'exists.')
    if icons is None:
        icons = random.sample(ICONS, 2)

    _room_dict[room_name] = GameState(room_name, [first_player], 'Team 1', 0,
                                      icons[0], [], 'Team 2', 0, icons[1])


def get_room_data(room_name: str, field: GameFields) -> Any:
    """Return a copy of a given room's game state."""

    assert game_room_exists(room_name), (f'Tried to get room state of '
                                         f'non-existent room {room_name}.')

    game_state = _room_dict[room_name]

    return getattr(game_state, field.value)


def update_room_data(room_name: str, field: GameFields, data: Any) -> None:
    """Update the field of some room's game state."""
    assert game_room_exists(room_name), f'Room {room_name} does not exist.'

    setattr(_room_dict[room_name], field.value, data)


def get_room_state(room_name: str) -> Dict[str, any]:
    """Get all game state data for a given room."""
    assert game_room_exists(room_name), f'Room {room_name} does not exist.'
    return asdict(_room_dict[room_name])


def clear_rooms() -> None:
    """Clear all game rooms from the database."""
    global _room_dict
    _room_dict = {}
