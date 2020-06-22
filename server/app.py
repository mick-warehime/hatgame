import logging
import random
import time
from typing import Dict, Any

from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

from server.app_utils import validate_fields
from server.icons import ICONS
from server.model.fields import ROOM_NAME, ERROR, PLAYER_NAME, GAME_STATE, \
    GameFields
from server.model.rooms import game_room_exists, get_room_data, \
    update_room_data, initialize_game_room, get_room_state

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=['http://127.0.0.1:8080',
                                               'http://0.0.0.0:8080',
                                               'http://stonebaby.herokuapp.com'])

counter = 0


@socketio.on("add_random", namespace='/')
def add_random(request):
    global counter
    logging.info("add_random {}".format(request))
    counter = counter + random.randint(1, 10)
    response = {'value': counter}
    logging.info("response {}".format(response))
    return response


@socketio.on("start_timer", namespace='/')
def toggle_timer(request):
    update(score=1)
    timer(request['duration'])


def timer(duration):
    count = 0
    while count < duration:
        time.sleep(1)
        emit('increment_timer')
        logging.info('increment timer')
        count += 1


@socketio.on("get_status", namespace='/')
def get_status():
    update()


@socketio.on('create_game', namespace='/')
def create_game(game_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a game creation request from a client.

    If a game with the specified name does not exist, create a game with that
    name. The room is populated by a single player with the specified name.
    This information is returned as a game_state message to the emitting client.

    If a game with the specified name already exists an error message is
    returned.
    If the game_request does not have the expected field, or a field is empty,
    then an error message is returned.


    Args:
        game_request: Request message with fields 'player name' and 'room name',
            defined as strings.


    Returns:
        A response message with either a 'game state' field or an 'error' field.
        The 'game state' field is a dictionary with fields defined in
        game_state.py. The error is sent only if a game room with the specified
        name already exists.
    """

    # Validate request
    error = validate_fields(game_request, (ROOM_NAME, PLAYER_NAME),
                            (ROOM_NAME, PLAYER_NAME))
    if error:
        return {ERROR: error}

    room_name = game_request[ROOM_NAME]
    if game_room_exists(room_name):
        return {ERROR: (f'Game room with name ({room_name}) '
                        f'already exists.')}

    initialize_game_room(room_name, game_request[PLAYER_NAME])
    return {GAME_STATE: get_room_state(room_name)}




def update(score=0):
    icons = ICONS.copy()
    random.shuffle(icons)
    icon1, icon2 = icons[0], icons[1]
    logging.info('GOT STATUS')
    response = {"team1": ["chad", "bardasd", "thad"],
                "icon1": icon1,
                "score1": score,
                "team2": ["brew", "drew", "agnew", "stu"],
                "icon2": icon2,
                "score2": 0}
    logging.info(response)
    emit('update_status', response)


if __name__ == '__main__':
    socketio.run(app=app, host='stonebaby.herokuapp.com')
