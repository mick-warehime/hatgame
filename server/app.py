import logging
import random
import time
from dataclasses import asdict
from typing import Dict

from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

from server.icons import ICONS
from server.model.fields import ROOM_NAME, ERROR, PLAYER_NAME, GAME_STATE
from server.model.game_state import build_game
from server.model.rooms import game_room_exists, add_game_room

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
def create_game(game_request: Dict[str, str]):
    """Receive and respond to a game request message from a client.

    If a game with the specified name does not exist, create a game with that
    name. The room is populated by a single player with the specified name.
    This information is returned as a game_state message to the emitting client.

    If a game with the specified name already exists, return an error message
    to the client.

    If the game_request does not have the expected fields, return an error
    message to the client.


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
    for field in (ROOM_NAME, PLAYER_NAME):
        if field not in game_request:
            return {ERROR: f'game request missing field ({field}).'}

    if game_room_exists(game_request[ROOM_NAME]):
        return {ERROR: (f'Game room with name ({game_request[ROOM_NAME]}) '
                        f'already exists.')}

    game_state = build_game(game_request[PLAYER_NAME], game_request[ROOM_NAME])
    add_game_room(game_state)
    return {GAME_STATE: asdict(game_state)}


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
