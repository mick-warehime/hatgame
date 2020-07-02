"""Tests of game creation / joining API"""
import pytest

from app.app import create_game
from app.controller.server_client_interface import join_game_action
from app.model.fields import (PLAYER_NAME, ROOM_NAME, ERROR, GAME_STATE)
from app.model.rooms import clear_rooms, game_room_exists, get_room_state


# Any pytest function that has setup as an argument invokes this method
@pytest.fixture
def setup():
    clear_rooms()
    yield None


def test_add_valid_game_room_creates_room(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)

    assert game_room_exists(room_name)
    assert player in result[GAME_STATE]['team_0_players']


def test_add_already_existing_game_room_gives_error(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)
    assert ERROR not in result

    result = create_game(request)
    assert ERROR in result
    assert 'already exists' in result[ERROR]


@pytest.mark.parametrize('field', (PLAYER_NAME, ROOM_NAME))
@pytest.mark.parametrize('empty_data', (False, True))
def test_create_game_missing_or_empty_data(setup, field, empty_data):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}
    if empty_data:
        request[field] = ''
    else:
        del request[field]

    result = create_game(request)
    assert ERROR in result
    if empty_data:
        assert 'must not evaluate to' in result[ERROR]
    else:
        assert 'missing field' in result[ERROR]


def test_create_then_join_one_player_per_team(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)
    assert ERROR not in result

    player2 = 'Dvir'
    result = join_game_action({PLAYER_NAME: player2, ROOM_NAME: room_name})
    assert ERROR not in result

    room = get_room_state(room_name)
    assert player in room.team_0_players
    assert player2 in room.team_1_players


def test_join_room_same_player_name(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)
    assert ERROR not in result

    result = join_game_action({PLAYER_NAME: player, ROOM_NAME: room_name})
    assert ERROR in result
    assert 'already in game' in result[ERROR]


def test_join_room_does_not_exist(setup):
    result = join_game_action({PLAYER_NAME: 'Mick', ROOM_NAME: 'Nonexistent'})
    assert ERROR in result
    assert 'does not exist' in result[ERROR]
