from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model.fields import PHRASES
from app.model.game_rooms import get_room
from app.model.player import build_player


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
    room = get_room(room_name)

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
    room.update_player(player_name, player_with_phrases)
