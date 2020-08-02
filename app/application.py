import logging
import os
import random
from typing import Dict, Any

from flask import render_template
from flask import session
from flask_socketio import join_room, leave_room

from app.actions import create_game_action, start_game_action, \
    next_clue_giver_action
from app.actions import force_room_update_action
from app.actions import join_game_action
from app.actions import leave_game_action
from app.actions import randomize_teams_action
from app.actions import submit_phrases_action
from app.actions import unready_phrases_action
from app.common.timer import timer
from app.initialization import create_app
from app.model.fields import Namespaces, ROOM_NAME, PLAYER_NAME, ERROR
from app.test_game import create_test_game

logging.basicConfig(level=logging.INFO)

counter = 0

app, socketio = create_app()
create_test_game()


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
    timer(request['duration'])


@socketio.on("force_room_update", namespace='/')
def force_room_update():
    force_room_update_action.force_room_update(session[ROOM_NAME])


@socketio.on(Namespaces.CREATE_GAME.value)
def create_game(create_request: Dict[str, str]) -> Dict[str, Any]:
    resp = create_game_action.create_game(create_request)
    if ERROR not in resp:
        initialize_session(create_request[PLAYER_NAME],
                           create_request[ROOM_NAME])
        force_room_update_action.force_room_update(create_request[ROOM_NAME])
    return resp


@socketio.on(Namespaces.JOIN_GAME.value)
def join_game(join_request: Dict[str, str]) -> Dict[str, Any]:
    resp = join_game_action.join_game(join_request)
    if ERROR not in resp:
        initialize_session(join_request[PLAYER_NAME], join_request[ROOM_NAME])
        force_room_update_action.force_room_update(join_request[ROOM_NAME])
    return resp


@socketio.on(Namespaces.RANDOMIZE_ROOM.value)
def randomize_room() -> Dict[str, Any]:
    room_name = session[ROOM_NAME]
    resp = randomize_teams_action.randomize_teams(room_name)
    if ERROR not in resp:
        force_room_update_action.force_room_update(room_name)
    return resp


@socketio.on(Namespaces.SUBMIT_PHRASES.value)
def submit_phrases(submit_request: Dict[str, Any]) -> Dict[str, Any]:
    room_name = session[ROOM_NAME]
    player_name = session[PLAYER_NAME]
    resp = submit_phrases_action.submit_phrases(room_name, player_name,
                                                submit_request)
    if ERROR not in resp:  # update because player is now ready.
        force_room_update_action.force_room_update(room_name)
    return resp


@socketio.on("unready_phrases")
def unready_phrases() -> None:
    room_name = session[ROOM_NAME]
    player_name = session[PLAYER_NAME]
    unready_phrases_action.unready_phrases(room_name, player_name)
    force_room_update_action.force_room_update(room_name)


def initialize_session(player_name: str, room_name: str) -> None:
    session[ROOM_NAME] = room_name
    session[PLAYER_NAME] = player_name
    join_room(room_name)


@socketio.on("disconnect", namespace='/')
def disconnect():
    leave_game()


@socketio.on("leave_game", namespace='/')
def leave_game():
    if ROOM_NAME not in session:
        return
    room_name = session[ROOM_NAME]
    player_name = session[PLAYER_NAME]
    leave_game_action.leave_game(player_name, room_name)
    force_room_update_action.force_room_update(room_name)
    leave_room(room_name)


@socketio.on(Namespaces.START_GAME.value, namespace='/')
def start_game(start_request: Dict[str, Any]):
    room_name = start_request[ROOM_NAME]
    start_game_action.start_game(room_name)
    force_room_update_action.force_room_update(room_name)


@socketio.on(Namespaces.NEXT_CLUE_GIVER.value, namespace='/')
def next_clue_giver(next_request: Dict[str, Any]) -> None:
    # update the next player
    room_name = next_request[ROOM_NAME]
    next_clue_giver_action.next_clue_giver(room_name)
    # send information to all clients
    force_room_update_action.force_room_update(room_name)


if __name__ == '__main__':
    host = '0.0.0.0' if os.getenv('FLASK_ENV') else 'stonebaby.herokuapp.com'
    socketio.run(app=app, host=host)
    create_test_game()
