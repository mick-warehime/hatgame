from random import shuffle
from typing import Dict, Any

from attr import evolve

from app.actions.validation_utils import validate_fields
from app.model import fields
from app.model.rooms import game_room_exists, get_room_state, update_room


def randomize_teams(room_name: str) -> Dict[str, str]:
    """Randomize the teams in a given room.

    If the room specified for randomization exists, the teams are randomized.
    The response message is empty. The new teams are always different.
    If the room does not exist or is not specified, a response message with an
    'error' field is returned.
    Args:
        room_name: the room to randomize.
    """
    if not game_room_exists(room_name):
        return {fields.ERROR: f'Room named {room_name} does not exist.'}

    room = get_room_state(room_name)
    players = list(room.team_2_players + room.team_1_players)
    num_players = len(players)
    shuffle(players)
    team_2_players = players[:num_players // 2]
    team_1_players = players[num_players // 2:]
    room = evolve(
        room,
        **dict(team_1_players=team_1_players, team_2_players=team_2_players))
    update_room(room_name, room)

    return {}
