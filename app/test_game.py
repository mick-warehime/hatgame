"""Implementation of server request/repsonse logic."""
from attr import evolve

from app.model import fields
from app.model.data_structures import build_player
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
    team_1 = [build_player(p) for p in ['Mick', 'Liz', 'M\'Lickz']]
    team_2 = [build_player(p) for p in ['Dvir', 'Celeste', 'Boaz', 'Ronen']]
    room = evolve(room, **dict(team_1_players=team_1, team_2_players=team_2))
    update_room(room_name, room)
