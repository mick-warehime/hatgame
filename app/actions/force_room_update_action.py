from flask_socketio import emit

from app.model.game_rooms import get_room


# allows client code to force pull new data
def force_room_update(room_name: str) -> None:
    """Update clients with new room information.

    Emits the following information:
    room: room name
    team1: Sequence of team 1 players
    team1_ready: Sequence of bools denoting which player is ready.
    icon1: Icon label for team 1
    score1: Score of team1
    (... equivalent data for team 2).


    """
    room = get_room(room_name)
    update_message = {
        "team1": [p.name for p in room.team_1_players],
        "team1_ready": [p.ready for p in room.team_1_players],
        "icon1": room.team_1_icon,
        "score1": room.team_1_score,
        "team2": [p.name for p in room.team_2_players],
        "team2_ready": [p.ready for p in room.team_2_players],
        "icon2": room.team_2_icon,
        "score2": room.team_2_score,
        "phrases": room.all_phrases(),
        "game_mode": room.game_mode,
        "game_round": room.game_round,
        "clue_giver": room.clue_giver,
        "last_clue_giver": room.last_clue_giver
    }
    emit('update_room', update_message, room=room_name)
