"""Implementation of server request/repsonse logic."""
from dataclasses import asdict
from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model import fields
from app.model.rooms import (game_room_exists, get_room_state,
                             initialize_game_room)


def create_game(create_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a game creation request from a client.

    If a game with the specified name does not exist, create a game with that
    name. The room is populated by a single player with the specified name.
    This information is returned as a game_state message to the emitting client.

    If a game with the specified name already exists an error message is
    returned.
    If the create_request does not have the expected field, or a field is empty,
    then an error message is returned.


    Args:
        create_request: Request message with fields 'player name' and 'room name',
            defined as strings.


    Returns:
        A response message with either a 'game state' field or an 'error' field.
        The 'game state' field is a dictionary with fields defined in
        game_state.py. The error is sent only if a game room with the specified
        name already exists.
    """

    # Validate request
    error = validate_fields(create_request,
                            (fields.ROOM_NAME, fields.PLAYER_NAME),
                            (fields.ROOM_NAME, fields.PLAYER_NAME))
    if error:
        return {fields.ERROR: error}

    room_name = create_request[fields.ROOM_NAME]
    if game_room_exists(room_name):
        return {fields.ERROR: (f'Game room with name ({room_name}) '
                               f'already exists.')}

    initialize_game_room(room_name, create_request[fields.PLAYER_NAME])
    return {fields.GAME_STATE: asdict(get_room_state(room_name))}
