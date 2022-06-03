import random

piece_score = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
CHECKMATE = 1000
STALEMATE = 0


def find_random_move(valid_moves) -> list:
    """Picks a random move from a list of valid moves

    :param valid_moves: list of legal chess moves that can be played
    :return: random move
    """
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move(game, valid_moves):
    """Finds the best move based on material

    :param game: the current chess game
    :param valid_moves: list of legal chess moves that can be played
    :return: the best move that can be currently played
    """
    turn_multiplier = 1 if game.current_turn.is_white_side else -1
    max_score = -CHECKMATE
    best_move = None

    promotion = True if game.promotion else False
    for player_move in valid_moves:
        if promotion:
            game.move_action(player_move[1], player_move[0])
        else:
            game.move_action(player_move[0][1], player_move[0][0])
            game.move_action(player_move[1][1], player_move[1][0])

        if game.is_checkmate():
            score = CHECKMATE
        elif game.is_stalemate():
            score = 0
        else:
            score = turn_multiplier * score_material(game.board)

        if score > max_score:
            max_score = score
            best_move = player_move

        game.undo_move()
    return best_move


def score_material(board):
    """Score the board based on material

    :param board: the chess board
    :return:
    """
    score = 0
    for row in board.boxes:
        for box in row:
            if box.piece is None:
                continue

            if box.piece.is_white:
                score += piece_score[str(box.piece)[1]]
            elif not box.piece.is_white:
                score -= piece_score[str(box.piece)[1]]
    return score
