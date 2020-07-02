import logging
import os
import random
import time
from typing import Dict, Any

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit

from app.controller import server_client_interface
from app.icons import ICONS
from app.model.fields import Namespaces

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='./static/dist',
            template_folder='./static/dist', static_url_path='')
socketio = SocketIO(app)
CORS(app)

counter = 0

server_client_interface.create_test_game()


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
    return server_client_interface.create_game_action(game_request)


@socketio.on(Namespaces.JOIN_GAME.value)
def join_game(join_request: Dict[str, str]) -> Dict[str, Any]:
    return server_client_interface.join_game_action(join_request)


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
