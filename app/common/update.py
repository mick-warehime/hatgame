import logging

from app.model.rooms import get_room_state


def update(room_name):
    logging.info('GOT STATUS')
    room = get_room_state(room_name)
    response = {"team1": room.team_1_players,
                "icon1": room.team_1_icon,
                "score1": room.team_1_score,
                "team2": room.team_2_players,
                "icon2": room.team_2_icon,
                "score2": room.team_2_score, }
    logging.info(response)
    emit('update_status', response)
