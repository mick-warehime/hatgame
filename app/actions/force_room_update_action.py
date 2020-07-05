from flask_socketio import emit

from app.model.rooms import get_room_state


# allows client code to force pull new data
def force_room_update(room_name):
    room = get_room_state(room_name)
    update_message = {"team1": room.team_1_players,
                      "icon1": room.team_1_icon,
                      "score1": room.team_1_score,
                      "team2": room.team_2_players,
                      "icon2": room.team_2_icon,
                      "score2": room.team_2_score}
    emit('update_room', update_message, room=room_name)
