"""Logic for handling multiple game rooms."""
import logging
from typing import Dict

from server.model.game_state import GameState

_room_dict: Dict[str, GameState] = {}


def game_room_exists(room_name: str) -> bool:
    """Whether a game room with the given name already exists."""
    return room_name in _room_dict


def add_game_room(game_state: GameState) -> None:
    """Adds a new game to the database of existing games.

    The game's name must not already exist in the database.
    """
    try:
        assert game_state.name not in _room_dict
    except AssertionError:
        logging.ERROR(f'Tried to add ({game_state.name}) but a room with that'
                      f' name already exists.')
        raise AssertionError

    _room_dict[game_state.name] = game_state


def clear_rooms() -> None:
    """Clear all game rooms from the database."""
    global _room_dict
    _room_dict = {}
