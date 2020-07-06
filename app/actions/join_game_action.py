"""Implementation of server request/repsonse logic."""
from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model import fields
from app.model.player import build_player
from app.model.rooms import (game_room_exists, get_room_state, update_room)


def join_game(join_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a join game request from a client.

    If the game room exists and the player name is not already in use, then
    the player is added to the game room. This is done by updating the game
    state in that room. The player is added to the team with fewest players.

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
    if any(plyr.name == player_name for plyr in room.all_players()):
        return {fields.ERROR: f'Player \'{player_name}\' already in game.'}

    # Add player to team with fewest members.
    if len(room.team_1_players) > len(room.team_2_players):
        room.team_2_players.append(build_player(player_name))
    else:
        room.team_1_players.append(build_player(player_name))
    update_room(room_name, room)
    return {}
