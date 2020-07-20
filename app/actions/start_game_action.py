"""Start the game from the lobby."""
from typing import Dict, Any

from attr import evolve

from app.model.game_rooms import game_room_exists, get_room, update_room
from app.model.room import GameModes


def start_game(room_name: str) -> Dict[str, Any]:
    """Change a room from lobby mode to the first mode of the round.

    Args:
        room_name: Name of the room to start game for. Must correspond to
            a room in lobby mode.

    """
    assert game_room_exists(room_name)

    room = get_room(room_name)

    assert room.game_mode == GameModes.LOBBY
    assert room.game_round == 0

    new_room = evolve(room, game_mode=GameModes.CLUE_GIVING_PRE, game_round=1)
    update_room(room_name, new_room)

    return {}
