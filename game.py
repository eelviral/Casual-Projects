import pygame
from board import Board
from move import Move
from player import Player
from pieces import *
from spot import Spot
import math
import copy

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
UI_SIZE = 0
IMAGES = {'white': {},
          'black': {}}


class GameStatus:
    ACTIVE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    FORFEIT = 3
    STALEMATE = 4
    RESIGNATION = 5


class Highlight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if x % 2 == 0:
            if y % 2 == 0:
                self.color = (227, 227, 118)
            else:
                self.color = (191, 207, 91)
        else:
            if y % 2 == 0:
                self.color = (191, 207, 91)
            else:
                self.color = (227, 227, 118)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x*SQ_SIZE,
                         self.y*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def __repr__(self):
        return f'({self.x} {self.y})'


class Game:
    players = []
    board = Board()
    move = []
    highlighted_boxes = []
    moves_played = []

    def __init__(self):
        self.length = self.width = WIDTH
        self.black = (77, 50, 34)
        self.white = (222, 184, 135)
        icon = pygame.image.load('./images/ico/chess-icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.length + UI_SIZE, self.width))
        pygame.display.set_caption('Chess Game')
        self.load_images()
        self._current_turn = None
        self._status = GameStatus.ACTIVE
        self.promotion = False
        self.promotion_pieces = []

    def init(self, p1, p2):
        if len(self.players) == 0:
            self.players.append(p1)
            self.players.append(p2)
        else:
            self.players[0] = p1
            self.players[1] = p2

        self.board.reset_board()
        self.board.update_controlled_squares()

        if p1.is_white_side:
            self.current_turn = p1
        else:
            self.current_turn = p2

        self.moves_played.clear()

    @property
    def status(self) -> int:
        """Get or set the GameStatus

        :return: bool
        """
        return self._status

    @status.setter
    def status(self, value) -> None:
        self._status = value

    @property
    def current_turn(self) -> Player:
        """Get or set the current player turn

        :return: Player
        """
        return self._current_turn

    @current_turn.setter
    def current_turn(self, value) -> None:
        self._current_turn = value

    def player_move(self, player, start_x, start_y, end_x, end_y) -> bool:
        start_box = self.board.get_box(start_x, start_y)
        if start_box.piece is None:
            return False

        end_box = self.board.get_box(end_x, end_y)
        move = Move(player, start_box, end_box)
        return self.make_move(move, player)

    def make_move(self, move, player) -> bool:
        start_piece = move.start.piece

        # Cannot move an empty box
        if start_piece is None:
            return False

        # Make sure next move prevents king from being in check
        if not isinstance(start_piece, King) and not self.protects_king(move.start, move.end):
            return False

        # Check if its player's turn
        if player != self.current_turn:
            return False
        if start_piece.is_white != player.is_white_side:
            return False

        # Check if piece can make this move
        if not start_piece.can_move(self.board, move.start, move.end):
            return False
        else:
            # Keep track of moves made by pawn for two step move/en passant or
            # moves made by rook and king for castling
            if isinstance(start_piece, (Pawn, King, Rook)):
                start_piece.moves_made += 1

        # Check if a piece is getting captured
        end_piece = move.end.piece
        if end_piece is not None:
            end_piece.captured = True
            move.piece_captured = end_piece
        else:
            if isinstance(start_piece, Pawn) and start_piece.en_passant:
                y = move.end.y - move.start.y
                end_piece = self.board.get_box(
                    move.start.x, move.start.y + y).piece
                move.piece_captured = end_piece

        # If a pawn moved two ranks, en passant is legal on this pawn on immediate move
        if start_piece is not None and isinstance(start_piece, Pawn):
            if start_piece.moves_made == 1 and start_piece.two_step_move:
                move.en_passant_legal = True
            elif start_piece.is_promoted:
                move.promotion_move = True
                self.promotion = True

        # Check if a pawn moved two ranks to perform en passant move
        if isinstance(start_piece, Pawn) and start_piece.en_passant:
            if (self.moves_played[-1].en_passant_legal and
                    self.moves_played[-1].end.y == move.end.y):
                x = move.end.x - move.start.x
                self.board.get_box(move.end.x - x, move.end.y).piece = None
                move.en_passant_move = True
                start_piece.en_passant = False
            else:
                start_piece.en_passant = False
                return False

        # Keep track of move
        self.moves_played.append(move)

        # Move the piece
        move.end.piece = move.start.piece
        move.start.piece = None

        # Check if a castling move is occurring
        if (start_piece is not None and isinstance(start_piece, King) and
                start_piece.is_castling):
            move.castling_move = True
            y = move.end.y - move.start.y
            rook_start = self.board.get_box(move.start.x, 0 if y < 0 else 7)
            rook_end = self.board.get_box(move.end.x, move.end.y + 1 if y < 0 else move.end.y - 1)

            rook_end.piece = rook_start.piece
            rook_start.piece = None
            start_piece.is_castling = False

        self.board.update_controlled_squares()

        # Game ends when King is captured
        if end_piece is not None and isinstance(end_piece, King):
            if player.is_white_side:
                self.status = GameStatus.WHITE_WIN
            else:
                self.status = GameStatus.BLACK_WIN

        # See if this move put opposing king in check and look for checkmate
        king_piece, king_box = self.board.get_king_box(not self.current_turn.is_white_side)
        if king_piece.risk_check(self.board, king_box.x, king_box.y):
            if self.is_checkmate():
                if player.is_white_side:
                    self.status = GameStatus.WHITE_WIN
                else:
                    self.status = GameStatus.BLACK_WIN
        else:
            if self.is_stalemate():
                self.status = GameStatus.STALEMATE

        # Let other player move next turn
        if self.current_turn == self.players[0]:
            self.current_turn = self.players[1]
        else:
            self.current_turn = self.players[0]

        self.board.update_controlled_squares()
        return True

    def protects_king(self, start, end) -> bool:
        start_piece = start.piece
        board = copy.deepcopy(self.board)
        board.get_box(end.x, end.y).piece = start_piece
        board.get_box(start.x, start.y).piece = None
        board.update_controlled_squares()

        king_piece, king_box = board.get_king_box(start_piece.is_white)
        if king_piece.risk_check(board, king_box.x, king_box.y):
            return False
        return True

    def is_checkmate(self) -> bool:
        # Get the squares controlled by the opposing player (the one who checked a king)
        op_controlled_squares = self.board.get_controlled_squares(self.current_turn.is_white_side)

        # Get the checked king based on current turn (opposite player)
        king_piece, king_box = self.board.get_king_box(not self.current_turn.is_white_side)

        # If checked king can move to defend itself, there is no checkmate
        for x, y in king_piece.controlled_squares(self.board, king_box.x, king_box.y):
            end_box = self.board.get_box(x, y)
            if (king_box.piece.can_move(self.board, king_box, end_box) and
                    self.protects_king(king_box, end_box)):
                return False

        # Look for a piece that can defend checked king
        for row in self.board.boxes:
            for box in row:
                if box.piece is None:
                    continue

                if box.piece.is_white == self.current_turn.is_white_side:
                    continue

                # If a piece can move to defend checked king, there is no checkmate
                for x, y in op_controlled_squares:
                    end_box = self.board.get_box(x, y)
                    if end_box.piece is not None and end_box.piece.is_white == self.current_turn.is_white_side:
                        continue

                    if box.piece.can_move(self.board, box, end_box) and self.protects_king(box, end_box):
                        return False
        return True

    def is_stalemate(self):
        piece_count = 0
        king_count = 0
        for row in self.board.boxes:
            for box in row:
                if box.piece is None:
                    continue
                else:
                    if isinstance(box.piece, King):
                        king_count += 1
                    piece_count += 1

        # If only two kings remain, its a stalemate
        if piece_count == 2 and king_count == 2:
            return True

        # Check if pieces can still make legal moves
        for row in self.board.boxes:
            for box in row:
                if box.piece is None:
                    continue

                if box.piece.is_white == self.current_turn.is_white_side:
                    continue

                if len(box.piece.legal_moves(self.board, box.x, box.y)) > 0:
                    return False
        return True

    @staticmethod
    def load_images() -> None:
        wb_pieces = [['white', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']],
                     ['black', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']]]
        for color, pieces in wb_pieces:
            for piece in pieces:
                IMAGES[color][piece] = pygame.transform.scale(
                    pygame.image.load(f'images/{color}/{piece}.png'),
                    (SQ_SIZE, SQ_SIZE))

    def draw_board(self) -> None:
        """
        Display black and white checkerboard background
        """
        size = SQ_SIZE
        count = 0
        for i in range(self.length + 1):
            columns = 0
            for j in range(self.length):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                        size * j, size * i, size, size])
                else:
                    pygame.draw.rect(self.screen, self.black, [
                        size * j, size * i, size, size])
                columns += 1
                count += 1
                if columns >= 8:
                    break
            count -= 1

        # Add highlighted boxes
        if len(self.highlighted_boxes) > 0:
            for box in self.highlighted_boxes:
                box.draw(self.screen)

        self.draw_labels()
        self.draw_pieces()

        if self.promotion:
            last_move = self.moves_played[-1]
            self.draw_promotion_options(last_move.end.x, last_move.end.y, last_move.piece_moved.is_white)
        pygame.display.update()

    def draw_pieces(self) -> None:
        boxes = self.board.boxes

        for row in boxes:
            for box in row:
                if box.piece is None:
                    continue

                color, piece = [i.lower() for i in repr(box.piece).split()]
                if box.piece.is_white:
                    self.screen.blit(IMAGES[color][piece],
                                     (box.y * SQ_SIZE, box.x * SQ_SIZE))
                else:
                    self.screen.blit(IMAGES[color][piece],
                                     (box.y * SQ_SIZE, box.x * SQ_SIZE))

    def draw_labels(self) -> None:
        font = pygame.font.SysFont('arial-bold', 23)
        row = self.board.boxes[-1]
        if self.board.white_top_spawn:
            letter_range = reversed(range(ord('a'), ord('i')))
        else:
            letter_range = range(ord('a'), ord('i'))
        for i, letter in enumerate(letter_range):
            if i % 2 == 0:
                ltr = font.render(chr(letter), True, self.white)
            else:
                ltr = font.render(chr(letter), True, self.black)
            self.screen.blit(ltr, ((row[i].y + 3.40/4) * SQ_SIZE, (row[i].x + 2.9/4) * SQ_SIZE))

        if self.board.white_top_spawn:
            col = [row[0] for row in self.board.boxes]
        else:
            col = [row[0] for row in self.board.boxes][::-1]
        for i in range(8):
            if (i % 2 == 0 and self.board.white_top_spawn) or (i % 2 != 0 and not self.board.white_top_spawn):
                num = font.render(str(i+1), True, self.black)
            else:
                num = font.render(str(i+1), True, self.white)
            self.screen.blit(num, (col[i].y * SQ_SIZE + SQ_SIZE * 1 / 20, col[i].x * SQ_SIZE + SQ_SIZE * 1 / 20))

    def draw_promotion_options(self, x, y, is_white):
        color = 'white' if is_white else 'black'
        promotion_images = [IMAGES[color]['queen'],
                            IMAGES[color]['rook'],
                            IMAGES[color]['bishop'],
                            IMAGES[color]['knight']]

        promotion_pieces = [Queen(is_white),
                            Rook(is_white),
                            Bishop(is_white),
                            Knight(is_white)]
        vector = 1 if x == 0 else -1
        for i in range(0, 4*vector, vector):
            pygame.draw.rect(self.screen, (255, 255, 255), (y * SQ_SIZE, (x + i) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            self.screen.blit(promotion_images[abs(i)], (y * SQ_SIZE, (x + i) * SQ_SIZE))

            if len(self.promotion_pieces) < 4:
                self.promotion_pieces.append(Spot((x + i), y, promotion_pieces[abs(i)]))

    def get_current_legal_moves(self) -> list:
        legal_moves = []
        for row in self.board.boxes:
            for box in row:
                if box.piece is None:
                    continue

                if box.piece.is_white != self.current_turn.is_white_side:
                    continue

                piece_legal_moves = box.piece.legal_moves(self.board, box.x, box.y)
                if len(piece_legal_moves) > 0:
                    for move in piece_legal_moves:
                        start = self.board.get_box(box.x, box.y)
                        end = self.board.get_box(move[0], move[1])
                        # Make sure to only include moves that dont put or keep king in check
                        if self.protects_king(start, end):
                            legal_moves.append([[box.x, box.y], move])
        return legal_moves

    def mouse_click(self, pos) -> None:
        """
        Chess Game's response to mouse click events

        :param pos: cursor position inside Chess Game window
        :return: None
        """
        mouse_x, mouse_y = [math.floor(i / SQ_SIZE) for i in pos]
        self.move_action(mouse_x, mouse_y)

    def move_action(self, move_x, move_y):
        if move_x > 7 or move_y > 7:
            return

        # Promotion
        if len(self.moves_played) > 0 and self.moves_played[-1].promotion_move and len(self.promotion_pieces) == 4:
            last_move = self.moves_played[-1]
            for spot in self.promotion_pieces:
                if spot.x == move_y and spot.y == move_x:
                    last_move.end.piece = spot.piece
                    self.promotion_pieces = []
                    self.promotion = False
            return

        selected_piece = self.board.get_box(move_y, move_x).piece

        # If a start piece has not been chosen
        if len(self.move) == 0:
            # Add start piece to move data if spot is not empty
            if selected_piece is not None and selected_piece.is_white == self.current_turn.is_white_side:
                self.move.append((move_x, move_y))
                self.highlighted_boxes.append(Highlight(move_x, move_y))
        # If a start piece has been chosen
        elif len(self.move) == 1:
            end_spot = self.board.get_box(
                self.move[0][1], self.move[0][0]).piece
            # Switch chosen start piece if player picks piece of same color
            if (selected_piece is not None and end_spot is not None) and selected_piece.is_white == end_spot.is_white:
                self.move[0] = (move_x, move_y)
                self.highlighted_boxes[-1] = Highlight(move_x, move_y)
            # Add end position to move data if spot is empty or has opposite color piece
            else:
                self.move.append((move_x, move_y))
                self.highlighted_boxes.append(Highlight(move_x, move_y))

        # If both a start and end piece have been chosen
        if len(self.move) == 2:
            # Check if the move is playable
            if self.player_move(self.current_turn, self.move[0][1],
                                self.move[0][0], self.move[1][1], self.move[1][0]):
                # Make sure that only the last move is recorded
                if len(self.highlighted_boxes) > 3:
                    self.highlighted_boxes = self.highlighted_boxes[2:]
            else:
                self.highlighted_boxes = self.highlighted_boxes[:-2]
            # Clear move data
            self.move.clear()
