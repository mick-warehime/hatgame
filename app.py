import logging
import random
import time

from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, template_folder='../client/static')
socketio = SocketIO(app, cors_allowed_origins='http://0.0.0.0:8080')

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
    timer(request['duration'])


def timer(duration):
    count = 0
    while count < duration:
        time.sleep(1)
        emit('increment_timer')
        logging.info('increment timer')
        count += 1
