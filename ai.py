import random


def find_random_move(valid_moves) -> list:
    """Picks a random move from a list of valid moves

    :param valid_moves: list of legal chess moves that can be played
    :return: random move
    """
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move():
    return
