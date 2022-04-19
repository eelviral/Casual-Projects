import pygame
from board import Board
from move import Move
from pieces import King, Pawn, Rook
import math
import copy

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
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
    current_turn = None
    move = []
    highlighted_boxes = []
    moves_played = []

    def __init__(self):
        self.length = self.width = WIDTH
        self.black = (77, 50, 34)
        self.white = (222, 184, 135)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')
        self.load_images()
        self._status = None

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
    def status(self) -> bool:
        """Get or set the GameStatus

        Returns: bool
        """
        return self._status

    @status.setter
    def status(self, value) -> None:
        self._status = value

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

        # Check if a castling move is occurring
        if (start_piece is not None and isinstance(start_piece, King)
                and start_piece.is_castling):
            move.castling_move = True
            y = move.end.y - move.start.y
            rook_start = self.board.get_box(move.start.x, 0 if y < 0 else 7)
            rook_end = self.board.get_box(move.start.x, move.end.y + 1 if y < 0 else move.end.y - 1)

            rook_end.piece = rook_start.piece
            rook_start.piece = None

        # If a pawn moved two ranks, en passant is legal on this pawn on immediate move
        if (start_piece is not None and isinstance(start_piece, Pawn)
                and start_piece.moves_made == 1 and start_piece.two_step_move):
            move.en_passant_legal = True

        # Check if a pawn moved two ranks to perform en passant move
        if isinstance(start_piece, Pawn) and start_piece.en_passant:
            if (self.moves_played[-1].en_passant_legal and
                    self.moves_played[-1].end.y == move.end.y):
                x = move.end.x - move.start.x
                self.board.get_box(move.end.x - x, move.end.y).piece = None
                move.en_passant_move = True
            else:
                start_piece.en_passant = False
                return False

        # Keep track of move
        self.moves_played.append(move)

        # Move the piece
        move.end.piece = move.start.piece
        move.end.controlled_squares = move.start.piece.controlled_squares(
            self.board, move.end.x, move.end.y)
        move.start.piece = None
        move.start.controlled_squares = None

        # See if this move put opposing king in check and look for checkmate
        king_piece, king_box = self.board.get_king_box(not self.current_turn.is_white_side)
        if king_piece.risk_check(self.board, king_box.x, king_box.y):
            if self.is_checkmate():
                if player.is_white_side:
                    self.status = GameStatus.WHITE_WIN
                else:
                    self.status = GameStatus.BLACK_WIN

        # Game ends when King is captured
        if end_piece is not None and isinstance(end_piece, King):
            if player.is_white_side:
                self.status = GameStatus.WHITE_WIN
            else:
                self.status = GameStatus.BLACK_WIN

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
        self.screen.fill(self.black)
        for i in range(self.length + 1):
            for j in range(self.length):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                        size * j, size * i, size, size])
                count += 1
            count -= 1

        # Add highlighted boxes
        if len(self.highlighted_boxes) > 0:
            for box in self.highlighted_boxes:
                box.draw(self.screen)

        self.draw_pieces()
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

    def mouse_click(self, pos) -> None:
        mouse_x, mouse_y = [math.floor(i / SQ_SIZE) for i in pos]
        selected_piece = self.board.get_box(mouse_y, mouse_x).piece

        # If a start piece has not been chosen
        if len(self.move) == 0:
            # Add start piece to move data if spot is not empty
            if selected_piece is not None and selected_piece.is_white == self.current_turn.is_white_side:
                self.move.append((mouse_x, mouse_y))
                self.highlighted_boxes.append(Highlight(mouse_x, mouse_y))
        # If a start piece has been chosen
        elif len(self.move) == 1:
            end_spot = self.board.get_box(
                self.move[0][1], self.move[0][0]).piece
            # Switch chosen start piece if player picks piece of same color
            if (selected_piece is not None and end_spot is not None) and selected_piece.is_white == end_spot.is_white:
                self.move[0] = (mouse_x, mouse_y)
                self.highlighted_boxes[-1] = Highlight(mouse_x, mouse_y)
            # Add end position to move data if spot is empty or has opposite color piece
            else:
                self.move.append((mouse_x, mouse_y))
                self.highlighted_boxes.append(Highlight(mouse_x, mouse_y))

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
