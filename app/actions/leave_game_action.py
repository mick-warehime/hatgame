from app.model.game_rooms import remove_player


def leave_game(player_name, room_name):
    remove_player(player_name, room_name)
