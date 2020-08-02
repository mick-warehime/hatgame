"""Action taking a room to its next mode in a cycle."""
from attr import evolve

from app.model.game_rooms import get_room, update_room
from app.model.room import GameModes


def next_mode(room_name: str) -> None:
    """Cause a room to change to its next mode in the cycle.
    
    The room must be in mode CLUE_GIVING or TURN_RECAP.
    The mode is iterated between the two modes.
    
    Args:
        room_name: The room to iterate.
    """

    room = get_room(room_name)

    modes = (GameModes.TURN_RECAP, GameModes.CLUE_GIVING)
    current_mode = room.game_mode
    assert current_mode in modes, (f'Next mode not defined for '
                                   f'{current_mode.name}')

    new_mode = modes[1 - modes.index(current_mode)]

    update_room(room_name, evolve(room, game_mode=new_mode))
