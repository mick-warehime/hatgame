from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model.fields import PHRASES
from app.model.player import build_player
from app.model.game_rooms import get_room_state


def submit_phrases(room_name, player_name,
                   submit_request: Dict[str, Any]) -> Dict[str, Any]:
    """Record phrases for a player and mark them as ready.

    If the submit request has a valid room, player name, and phrases, update
    the room with those phrases and mark the player as ready. Empty phrases
    are not added.

    Otherwise, an error is returned if a phrase is repeated (or has already been
    submitted).

    Args:
        room_name: The room that this update will impact.
        player_name: The player submitting the phrases.
        submit_request: Message with fields PLAYER_NAME and PHRASES.
             The PHRASES field should store a sequence of string phrases.

    """

    # Validate message structure
    error = validate_fields(submit_request, (PHRASES,), (PHRASES,))
    if error:
        raise ValueError(error)

    # get player from name
    room = get_room_state(room_name)

    player_found = False
    for player in room.all_players():
        if player_name == player.name:
            player_found = True
    if not player_found:
        raise ValueError(f'Player {player_name} not in room {room_name}.')

    # check phrases
    phrases = submit_request[PHRASES]

    # update player as ready, with phrases
    player_with_phrases = build_player(player_name, True, phrases)
    team_1_names = [p.name for p in room.team_1_players]
    if player_name in team_1_names:
        ind = team_1_names.index(player_name)
        room.team_1_players[ind] = player_with_phrases
        return {}
    team_2_names = [p.name for p in room.team_2_players]
    if player_name in team_2_names:
        ind = team_2_names.index(player_name)
        room.team_2_players[ind] = player_with_phrases
        return {}
    raise ValueError(f'Player should be in team but is not: {player_name}')
