"""Tests of game creation API"""
import pytest

from server.app import create_game
from server.model.fields import PLAYER_NAME, ROOM_NAME, ERROR, GAME_STATE
from server.model.rooms import clear_rooms, game_room_exists


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
