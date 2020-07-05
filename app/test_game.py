"""Implementation of server request/repsonse logic."""
from dataclasses import replace

from app.model import fields
from app.model.rooms import (game_room_exists, get_room_state,
                             initialize_game_room, update_room)


def create_test_game() -> None:
    """Add a test game to the data model.

    The game has room name 'test' and is populated with random characters.
    If the game already exists then this function does nothing.
    """

    room_name = fields.TEST_GAME
    if game_room_exists(room_name):
        return

    # initialize room
    initialize_game_room(room_name, 'Mick')

    # populate room with players
    room = get_room_state(room_name)
    room = replace(
        room,
        **dict(team_1_players=['Mick', 'Liz', 'M\'Lickz'],
               team_2_players=['Dvir', 'Celeste', 'Boaz', 'Ronen']))
    update_room(room_name, room)
