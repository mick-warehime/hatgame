import logging
import os
import random
from typing import Dict, Any

from flask import render_template

from app.actions import create_game_action
from app.actions import force_room_update_action
from app.actions import join_game_action
from app.common.timer import timer
from app.initialization import create_app
from app.model.fields import Namespaces
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
    force_room_update_action.force_room_update()


@socketio.on(Namespaces.CREATE_GAME.value)
def create_game(create_request: Dict[str, str]) -> Dict[str, Any]:
    return create_game_action.create_game(create_request)


@socketio.on(Namespaces.JOIN_GAME.value)
def join_game(join_request: Dict[str, str]) -> Dict[str, Any]:
    return join_game_action.join_game(join_request)


if __name__ == '__main__':
    host = '0.0.0.0' if os.getenv('FLASK_ENV') else 'stonebaby.herokuapp.com'
    socketio.run(app=app, host=host)
    create_test_game()
