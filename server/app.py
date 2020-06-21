import logging
import random
import time

from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

from icons import ICONS

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=['https://127.0.0.1:8080', 'https://0.0.0.0:8080',
                                               'https://stonebaby.herokuapp.com'])

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
    socketio.run(app=app)
