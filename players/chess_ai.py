# import random
# import pickle

# from board import Board
# from game import Game

# piece_score = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
# CHECKMATE = 1000
# STALEMATE = 0
# EPSILON = 0.2  # exploration rate
# ALPHA = 0.5  # learning rate
# GAMMA = 0.9  # discount factor

# try:
#     with open('q_learning_data.pkl', 'rb') as file:
#         data = pickle.load(file)
#         q_table = data['q_table']
#         generation = data['generation']
#         print(generation)
# except FileNotFoundError:
#     # Initialize Q-table as an empty dictionary if the file doesn't exist
#     q_table = {}
#     generation = 5


# def save():
#     global generation
#     generation += 1
#     with open('q_learning_data.pkl', 'wb') as f:
#         pickle.dump({'q_table': q_table, 'generation': generation}, f)


# def find_random_move(valid_moves: list[list]) -> list:
#     """Picks a random move from a list of valid moves

#     :param valid_moves: list of legal chess moves that can be played
#     :return: random move
#     """
#     return valid_moves[random.randint(0, len(valid_moves) - 1)]


# def find_best_move(game: Game, valid_moves):
#     """Finds the best move based on material.

#     :param game: the current chess game
#     :param valid_moves:
#     :return: the best move that can be currently played
#     """
#     state = get_state(game)
#     if random.uniform(0, 1) < EPSILON:  # Exploration
#         move = tuple(map(tuple, random.choice(valid_moves)))  # ensure it's a tuple of tuples
#     else:  # Exploitation
#         move = max(valid_moves, key=lambda x: get_q_value(state, tuple(map(tuple, x))))  # ensure it's a tuple of tuples

#     start_pos, end_pos = move  # Assuming move is a tuple of tuples
#     game.player_move(game.current_turn, start_pos[0], start_pos[1], end_pos[0], end_pos[1])

#     new_state = get_state(game)
#     reward = score_material(game.board)
#     update_q_value(state, move, reward, game)
#     return move


# def get_state(game: Game):
#     """Returns a state representation for the current game state.

#     :param game: the current chess game
#     :return: a representation of the current game state
#     """
#     board_str = str(game.board)
#     turn_bool = game.current_turn.is_white_side
#     return board_str, turn_bool


# def score_material(board: Board):
#     """Score the board based on material

#     :param board: the chess board
#     :return:
#     """
#     score = 0
#     for row in board.boxes:
#         for box in row:
#             if box.piece is None:
#                 continue

#             if box.piece.is_white:
#                 score += piece_score[str(box.piece)[1]]
#             elif not box.piece.is_white:
#                 score -= piece_score[str(box.piece)[1]]
#     return score


# def get_q_value(state, action):
#     """Returns the Q-value for a given state-action pair.

#     :param state: The current state.
#     :param action: The action taken.
#     :return: The Q-value for the given state-action pair.
#     """
#     return q_table.get((state, action), 0.0)


# def update_q_value(state, action, reward, game):
#     """Updates the Q-value for a given state-action pair based on the reward and the maximum Q-value for the new state.

#     :param state: The current state.
#     :param action: The action taken.
#     :param reward: The reward received for taking the action.
#     :param game: The game object instance.
#     """
#     new_state = get_state(game)
#     max_q_new_state = max([get_q_value(new_state, tuple(map(tuple, a))) for a in game.get_current_legal_moves()])
#     current_q_value = get_q_value(state, tuple(map(tuple, action)))  # convert action to tuple of tuples
#     new_q_value = (1 - ALPHA) * current_q_value + ALPHA * (reward + GAMMA * max_q_new_state)
#     q_table[(state, tuple(map(tuple, action)))] = new_q_value  # use tuple of tuples for action here as well

