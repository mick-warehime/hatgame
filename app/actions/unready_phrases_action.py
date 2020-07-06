from typing import Dict, Any

from app.model.player import build_player
from app.model.rooms import get_room_state


def unready_phrases(room_name, player_name) -> Dict[str, Any]:
    """Remove phrases for a player and mark them as unready.

    Args:
        room_name: The room that this update will impact.
        player_name: The player submitting the phrases.
    """

    # get player from name
    room = get_room_state(room_name)

    player = None
    player_found = False
    for player in room.all_players():
        if player_name == player.name:
            player_found = True
    if not player_found:
        raise ValueError(f'Player {player_name} not in room {room_name}.')

    # check phrases

    # update player as ready, with phrases
    player_with_phrases = build_player(player_name, False, [])
    if player in room.team_1_players:
        ind = room.team_1_players.index(player)
        room.team_1_players[ind] = player_with_phrases
    if player in room.team_2_players:
        ind = room.team_2_players.index(player)
        room.team_2_players[ind] = player_with_phrases

    return {}
