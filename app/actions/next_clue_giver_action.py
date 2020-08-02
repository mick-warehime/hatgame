from attr import evolve

from app.model.game_rooms import game_room_exists, get_room, update_room


def next_clue_giver(room_name: str) -> {}:
    """Changes the clue giver in a room to the next one in the order.

    The clue giver is set to the next person on the other team. If the
    other team is empty the next player on the current team is chosen.

    Args:
        room_name: The room for which to iterate the clue giver.
    """
    assert game_room_exists(room_name)

    room = get_room(room_name)

    next_giver = None
    prev_giver = room.last_clue_giver  # the one before current

    teams = (room.team_1_players, room.team_2_players)
    # special processing to handle no previous giver. Pretend like the previous
    # giver for the other team is the last person on that team.
    if prev_giver is None:
        if room.clue_giver in teams[0]:
            other_team = teams[1]
        else:
            assert room.clue_giver in teams[1], (f'Clue giver {room.clue_giver}'
                                                 f' missing.')
            other_team = teams[0]

        if not other_team:  # switch to next player on current player's team
            prev_giver = room.clue_giver
        else:
            prev_giver = other_team[-1]

    # next clue giver is one following last_clue_giver (same team)
    for team in teams:

        if prev_giver in team:
            ind = team.index(prev_giver)
            next_giver = team[(ind + 1) % len(team)]

    update_room(room.name, evolve(room, last_clue_giver=room.clue_giver,
                                  clue_giver=next_giver))
