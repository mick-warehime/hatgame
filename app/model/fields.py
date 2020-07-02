"""Enumeration of fields used in different messages"""
from enum import Enum

ERROR = 'error'
ROOM_NAME = 'room name'
PLAYER_NAME = 'player name'
GAME_STATE = 'game state'


# Enumeration of all namespaces used with socketio.
class Namespaces(Enum):
    CREATE_GAME = '/create_game'
    JOIN_GAME = '/join_game_action'
    PLAYER_JOINED = '/player_joined'
