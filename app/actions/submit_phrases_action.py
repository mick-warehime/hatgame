from typing import Dict, Any

from app.actions.validation_utils import validate_fields
from app.model.data_structures import build_player
from app.model.fields import PLAYER_NAME, PHRASES, ROOM_NAME, ERROR
from app.model.rooms import game_room_exists, get_room_state


def submit_phrases(submit_request: Dict[str, Any]) -> Dict[str, Any]:
    """Record phrases for a build_player and mark them as ready.

    If the submit request has a valid room, player name, and phrases, update
    the room with those phrases and mark the player as ready. Empty phrases
    are not added.

    Otherwise, an error is returned if the room does not exist, if the player
    is not in the room, if a phrase is repeated (or has already been
    submitted) or is empty, or if a required field is missing.

    Args:
        submit_request: Message with fields ROOM_NAME, PLAYER_NAME and PHRASES.
             The PHRASES field should store a sequence of string phrases.

    """

    # Validate message structure
    error = validate_fields(submit_request, (ROOM_NAME, PHRASES, PLAYER_NAME),
                            (ROOM_NAME, PHRASES, PLAYER_NAME))
    if error:
        return {ERROR: error}

    room_name = submit_request[ROOM_NAME]
    if not game_room_exists(room_name):
        return {ERROR: f'Room {room_name} does not exist.'}

    # get player from name
    room = get_room_state(room_name)
    player_name = submit_request[PLAYER_NAME]

    player = None
    player_found = False
    for player in room.all_players():
        if player_name == player.name:
            player_found = True
    if not player_found:
        return {ERROR: f'Player {player_name} not in room {room_name}.'}
    assert not player.ready

    # check phrases
    existing_phrases = room.all_phrases()
    phrases = submit_request[PHRASES]
    for phrase in phrases:
        if phrase in existing_phrases:
            return {ERROR: f'"{phrase}" already submitted.'}
    if len(phrases) != len(set(phrases)):
        return {ERROR: 'Phrases may not be repeated.'}

    # update player as ready, with phrases
    new_player = build_player(player_name, True, phrases)
    if player in room.team_1_players:
        ind = room.team_1_players.index(player)
        room.team_1_players[ind] = new_player
    if player in room.team_2_players:
        ind = room.team_2_players.index(player)
        room.team_2_players[ind] = new_player

    return {}
