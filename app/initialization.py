from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__,
                static_folder='./../static/dist',
                template_folder='./../static/dist',
                static_url_path='')
    socketio = SocketIO(app)
    CORS(app)
    return app, socketio
