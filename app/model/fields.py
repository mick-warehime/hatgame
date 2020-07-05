"""Enumeration of fields used in different messages"""
from enum import Enum

ERROR = 'error'
ROOM_NAME = 'room'
PLAYER_NAME = 'player'
GAME_STATE = 'game_state'
TEST_GAME = 'asdf'


# Enumeration of all namespaces used with socketio.
class Namespaces(Enum):
    CREATE_GAME = 'create_game'
    JOIN_GAME = 'join_game'
    ROOM_UPDATED = 'room_updated'
