"""Implementation of server request/repsonse logic."""
from typing import Dict, Any

from flask_socketio import emit

from app.app_utils import validate_fields
from app.model import fields
from app.model.rooms import (game_room_exists, get_room_data,
                             update_room_data, get_room_state,
                             initialize_game_room)


def join_game_action(join_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a join game request from a client.

    If the game room exists and the player name is not already in use, then
    the player is added to the game room. This is done by updating the game
    state in that room and broadcasting the new state to all clients (
    namespace 'player_joined'). The player is added to the team with fewest
    players.

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
    team_0_players = get_room_data(room_name, fields.GameFields.TEAM_0_PLAYERS)
    team_1_players = get_room_data(room_name, fields.GameFields.TEAM_1_PLAYERS)

    player_name = join_request[fields.PLAYER_NAME]
    if player_name in team_0_players or player_name in team_1_players:
        return {fields.ERROR: f'Player named {player_name} already in game.'}

    # Add player to team with fewest members.
    if len(team_0_players) > len(team_1_players):
        team_1_players += (player_name,)
        update_room_data(room_name, fields.GameFields.TEAM_1_PLAYERS,
                         team_1_players)
    else:
        team_0_players += (player_name,)
        update_room_data(room_name, fields.GameFields.TEAM_0_PLAYERS,
                         team_0_players)

    # Emit new game state to all clients.
    emit(fields.Namespaces.PLAYER_JOINED.value, get_room_state(room_name),
         broadcast=True)

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
        return {fields.ERROR: (f'Game room with name ({room_name}) '
                               f'already exists.')}

    initialize_game_room(room_name, game_request[fields.PLAYER_NAME])
    return {fields.GAME_STATE: get_room_state(room_name)}
