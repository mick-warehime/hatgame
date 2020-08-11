from flask_socketio import emit

from app.model.game_rooms import get_room
from app.model.room import convert_room_to_json


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

    emit('update_room', convert_room_to_json(room), room=room_name)
