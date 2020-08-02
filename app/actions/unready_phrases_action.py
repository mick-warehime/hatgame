from typing import Dict, Any

from app.model.game_rooms import get_room
from app.model.player import build_player


def unready_phrases(room_name, player_name) -> Dict[str, Any]:
    """Remove phrases for a player and mark them as unready.

    Args:
        room_name: The room that this update will impact.
        player_name: The player submitting the phrases.
    """

    # get player from name
    room = get_room(room_name)

    player_found = False
    for player in room.all_players():
        if player_name == player.name:
            player_found = True
    if not player_found:
        raise ValueError(f'Player {player_name} not in room {room_name}.')

    # check phrases

    # update player as ready, with phrases
    player_with_phrases = build_player(player_name, False, [])
    room.update_player(player_name, player_with_phrases)

    return {}
