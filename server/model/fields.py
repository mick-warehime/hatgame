"""Enumeration of fields used in different messages"""
from enum import Enum

ERROR = 'error'
ROOM_NAME = 'room name'
PLAYER_NAME = 'player name'
GAME_STATE = 'game state'


class GameFields(Enum):
    NAME = 'name'
    TEAM_0_PLAYERS = 'team_0_players'
    TEAM_0_NAME = 'team_0_name'
    TEAM_0_SCORE = 'team_0_score'
    TEAM_0_ICON = 'team_0_icon'
    TEAM_1_PLAYERS = 'team_1_players'
    TEAM_1_NAME = 'team_1_name'
    TEAM_1_SCORE = 'team_1_score'
    TEAM_1_ICON = 'team_1_icon'