from flask import session

from app.model import fields
from app.model.rooms import get_room_state
from app.model.rooms import update_room


# allows client code to force pull new data
def force_room_update():
    room_name = session[fields.ROOM_NAME]
    room = get_room_state(room_name)
    update_room(room_name, room)
