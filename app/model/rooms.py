"""Logic for handling multiple game rooms."""
import random
from typing import Dict, Tuple

from app.icons import ICONS
from app.model.room import Room

_room_dict: Dict[str, Room] = {}


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

    _room_dict[room_name] = Room(room_name, (first_player,), 0,
                                 icons[0], (), 0, icons[1])


def update_room(room_name: str, data: Room) -> None:
    """Update specific room fields."""
    assert game_room_exists(room_name), f'Room {room_name} does not exist.'

    _room_dict[room_name] = data


def get_room_state(room_name: str) -> Room:
    """Get all game state data for a given room."""
    assert game_room_exists(room_name), f'Room {room_name} does not exist.'
    return _room_dict[room_name]


def clear_rooms() -> None:
    """Clear all game rooms from the database."""
    global _room_dict
    _room_dict = {}
