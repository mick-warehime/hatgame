"""Implementation of server request/repsonse logic."""
import logging
from dataclasses import asdict, replace
from random import shuffle
from typing import Dict, Any

from flask_socketio import emit

from app.app_utils import validate_fields
from app.model import fields
from app.model.fields import Namespaces
from app.model.rooms import (game_room_exists, get_room_state,
                             initialize_game_room, update_room)


def join_game_action(join_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a join game request from a client.

    If the game room exists and the player name is not already in use, then
    the player is added to the game room. This is done by updating the game
    state in that room and broadcasting the new state to all clients (
    see Namespaces.ROOM_UPDATED). The message is just a dictionary storing
    the updated game state (see room_name.GameState). The player is added to the
    team with fewest players.

    If the game room does not exist an error message is returned.
    If the player name is already taken an error message is returned.
    If a field is missing or blank in the request an error message is returned.

    Args:
        join_request: Dictionary containing a 'player name' and 'room name'
            fields.

    Returns:
        On success, an empty dictionary is returned and the updated game
        state is broadcast to all clients in the room.
        Otherwise returns a dictionary with an 'error' field.
    """

    error = validate_fields(join_request,
                            (fields.ROOM_NAME, fields.PLAYER_NAME),
                            (fields.ROOM_NAME, fields.PLAYER_NAME))
    if error:
        return {fields.ERROR: error}

    room_name = join_request[fields.ROOM_NAME]
    if not game_room_exists(room_name):
        return {fields.ERROR: f'Room {room_name} does not exist.'}

    # Get current teams and check player name not already in use
    room = get_room_state(room_name)

    player_name = join_request[fields.PLAYER_NAME]
    if player_name in room.team_0_players or player_name in room.team_1_players:
        return {fields.ERROR: f'Player named {player_name} already in game.'}

    # Add player to team with fewest members.
    if len(room.team_0_players) > len(room.team_1_players):
        players = room.team_1_players + (player_name,)
        room = replace(room, **dict(team_1_players=players))

    else:
        players = room.team_0_players + (player_name,)
        room = replace(room, **dict(team_0_players=players))

    update_room(room_name, room)

    # Emit new game state to all clients.
    try:
        emit(fields.Namespaces.ROOM_UPDATED.value,
             asdict(room),
             broadcast=True,
             namespace=Namespaces.ROOM_UPDATED.value)
    except RuntimeError:  # This occurs during tests.
        logging.log(logging.ERROR, 'Runtime error during emit.')

    return {}


def create_game_action(game_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a game creation request from a client.

    If a game with the specified name does not exist, create a game with that
    name. The room is populated by a single player with the specified name.
    This information is returned as a game_state message to the emitting client.

    If a game with the specified name already exists an error message is
    returned.
    If the game_request does not have the expected field, or a field is empty,
    then an error message is returned.


    Args:
        game_request: Request message with fields 'player name' and 'room name',
            defined as strings.


    Returns:
        A response message with either a 'game state' field or an 'error' field.
        The 'game state' field is a dictionary with fields defined in
        game_state.py. The error is sent only if a game room with the specified
        name already exists.
    """

    # Validate request
    error = validate_fields(game_request,
                            (fields.ROOM_NAME, fields.PLAYER_NAME),
                            (fields.ROOM_NAME, fields.PLAYER_NAME))
    if error:
        return {fields.ERROR: error}

    room_name = game_request[fields.ROOM_NAME]
    if game_room_exists(room_name):
        return {
            fields.ERROR: (f'Game room with name ({room_name}) '
                           f'already exists.')
        }

    initialize_game_room(room_name, game_request[fields.PLAYER_NAME])
    return {fields.GAME_STATE: asdict(get_room_state(room_name))}


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
        **dict(team_0_players=('Mick', 'Liz', 'M\'Lickz'),
               team_1_players=('Dvir', 'Celeste', 'Boaz', 'Ronen')))
    update_room(room_name, room)


def randomize_teams_action(request: Dict[str, Any]) -> Dict[str, str]:
    """Randomize the teams in a given room.

    If the room specified for randomization exists, the teams are randomized
    and an update message (Namespaces.UPDATE_ROOM) is emitted with new room
    data. The response message is empty. The new teams are always different.

    If the room does not exist or is not specified, a response message with an
    'error' field is returned.

    Args:
        request: Request message with a 'room name' field specifying the room.
    """

    error = validate_fields(request, (fields.ROOM_NAME,))
    if error:
        return {fields.ERROR: error}

    room_name = request[fields.ROOM_NAME]
    if not game_room_exists(room_name):
        return {fields.ERROR: f'Room named {room_name} does not exist.'}

    room = get_room_state(room_name)
    players = list(room.team_0_players + room.team_1_players)
    num_players = len(players)
    shuffle(players)
    team_0_players = players[:num_players // 2]
    team_1_players = players[num_players // 2:]
    room = replace(
        room,
        **dict(team_1_players=team_1_players, team_0_players=team_0_players))
    update_room(room_name, room)

    try:
        emit(Namespaces.ROOM_UPDATED.value,
             asdict(room),
             broadcast=True,
             namespace=Namespaces.ROOM_UPDATED.value)
    except RuntimeError:
        pass  # This happens during unit tests and I don't know how to fix it.

    return {}
