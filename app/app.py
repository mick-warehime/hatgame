import logging
import os
import random
import time
from typing import Dict, Any

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit

from app.icons import ICONS
from server.app_utils import validate_fields
from server.model.fields import (ROOM_NAME, ERROR, PLAYER_NAME, GAME_STATE,
                                 GameFields, Namespaces)
from server.model.rooms import (game_room_exists, initialize_game_room,
                                get_room_state, get_room_data, update_room_data)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='./static/dist', template_folder='./static/dist', static_url_path='')
socketio = SocketIO(app)
CORS(app)

counter = 0

@app.route('/')
def index():
    return render_template('index.html')


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


@socketio.on(Namespaces.CREATE_GAME.value)
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


@socketio.on(Namespaces.JOIN_GAME.value)
def join_game(join_request: Dict[str, str]) -> Dict[str, Any]:
    """Receive and respond to a join game request from a client.

    If the game room exists and the player name is not already in use, then
    the player is added to the game room. This is done by updating the game
    state in that room and broadcasting the new state to all clients (
    namespace 'player_joined'). The player is added to the team with fewest
    players.

    If the game room does not exist an error message is returned.
    If the player name is already taken an error message is returned.
    If a field is missing or blank in the request an error message is returned.

    Args:
        join_request: Dictionary containing a 'player name' and 'room name'
            fields.

    Returns:
        On success, an empty dictionary is returned and the updated game
        state is broadcast to all clients in the room.
        Otherwise returns a dictionary with an 'error' field.
    """

    error = validate_fields(join_request, (ROOM_NAME, PLAYER_NAME),
                            (ROOM_NAME, PLAYER_NAME))
    if error:
        return {ERROR: error}

    room_name = join_request[ROOM_NAME]
    if not game_room_exists(room_name):
        return {ERROR: f'Room {room_name} does not exist.'}

    # Get current teams and check player name not already in use
    team_0_players = get_room_data(room_name, GameFields.TEAM_0_PLAYERS)
    team_1_players = get_room_data(room_name, GameFields.TEAM_1_PLAYERS)

    player_name = join_request[PLAYER_NAME]
    if player_name in team_0_players or player_name in team_1_players:
        return {ERROR: f'Player named {player_name} already in game.'}

    # Add player to team with fewest members.
    if len(team_0_players) > len(team_1_players):
        team_1_players += (player_name,)
        update_room_data(room_name, GameFields.TEAM_1_PLAYERS, team_1_players)
    else:
        team_0_players += (player_name,)
        update_room_data(room_name, GameFields.TEAM_0_PLAYERS, team_0_players)

    # Emit new game state to all clients.
    socketio.emit(Namespaces.PLAYER_JOINED.value, get_room_state(room_name),
                  broadcast=True)

    return {}


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
    host = '0.0.0.0' if os.getenv('FLASK_ENV') else 'stonebaby.herokuapp.com'
    socketio.run(app=app, host=host)
