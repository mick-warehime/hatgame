"""Tests of game creation / joining API"""
import random

import pytest

from app.actions.create_game_action import create_game
from app.actions.join_game_action import join_game
from app.actions.randomize_teams_action import randomize_teams
from app.model.player import build_player
from app.model.fields import (PLAYER_NAME, ROOM_NAME, GAME_STATE,
                              TEST_GAME, ERROR)
from app.model.game_rooms import clear_rooms, game_room_exists, get_room
from app.test_game import create_test_game


# Any pytest function that has setup as an argument invokes this method
@pytest.fixture
def setup():
    clear_rooms()
    yield None


def test_room_created():
    create_test_game()
    assert game_room_exists(TEST_GAME)

    room = get_room(TEST_GAME)
    assert build_player('Mick') in room.team_1_players
    assert build_player('Dvir') in room.team_2_players


def test_randomize_room():
    create_test_game()

    room = get_room(TEST_GAME)
    team_2 = room.team_2_players
    team_1 = room.team_1_players
    # Using a seed here ensures the teams will change.
    random.seed(11)
    randomize_teams(TEST_GAME)

    room = get_room(TEST_GAME)
    assert team_2 != room.team_2_players
    assert team_1 != room.team_1_players


def test_add_valid_game_room_creates_room(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)

    assert game_room_exists(room_name)
    team_1_players = result[GAME_STATE]['team_1_players']
    assert any(p['name'] == player for p in team_1_players)


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
    result = join_game({PLAYER_NAME: player2, ROOM_NAME: room_name})
    assert ERROR not in result

    room = get_room(room_name)
    assert build_player(player) in room.team_1_players
    assert build_player(player2) in room.team_2_players


def test_join_room_same_player_name(setup):
    room_name = 'room'
    player = 'Mick'
    request = {PLAYER_NAME: player, ROOM_NAME: room_name}

    result = create_game(request)
    assert ERROR not in result

    result = join_game({PLAYER_NAME: player, ROOM_NAME: room_name})
    assert ERROR in result
    assert 'already in game' in result[ERROR]


def test_join_room_does_not_exist(setup):
    result = join_game({PLAYER_NAME: 'Mick', ROOM_NAME: 'Nonexistent'})
    assert ERROR in result
    assert 'does not exist' in result[ERROR]
