from dataclasses import replace
from random import shuffle
from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model import fields
from app.model.rooms import game_room_exists, get_room_state, update_room


def randomize_teams(request: Dict[str, Any]) -> Dict[str, str]:
    """Randomize the teams in a given room.

    If the room specified for randomization exists, the teams are randomized.
    The response message is empty. The new teams are always different.
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
    players = list(room.team_2_players + room.team_1_players)
    num_players = len(players)
    shuffle(players)
    team_2_players = players[:num_players // 2]
    team_1_players = players[num_players // 2:]
    room = replace(
        room,
        **dict(team_1_players=team_1_players, team_2_players=team_2_players))
    update_room(room_name, room)

    return {}
