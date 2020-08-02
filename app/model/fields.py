"""Enumeration of fields used in different messages"""
from enum import Enum

ERROR = 'error'
ROOM_NAME = 'room'
PLAYER_NAME = 'player'
GAME_STATE = 'game_state'
TEST_GAME = 'asdf'
PHRASES = 'phrases'


# Enumeration of all namespaces used with socketio.
class Namespaces(Enum):
    CREATE_GAME = 'create_game'
    JOIN_GAME = 'join_game'
    ROOM_UPDATED = 'room_updated'
    RANDOMIZE_ROOM = 'randomize_room'
    SUBMIT_PHRASES = 'submit_phrases'
    NEXT_CLUE_GIVER = 'next_clue_giver'
