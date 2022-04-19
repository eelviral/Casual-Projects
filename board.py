from spot import Spot
from pieces import *


class Board:
    def __init__(self):
        super().__init__()
        self.boxes = []
        self._king_pieces = {'white': Spot(0, 0),
                             'black': Spot(0, 0)}

    def get_box(self, x, y) -> Spot:
        if (x < 0 or x > 7) or (y < 0 or y > 7):
            raise Exception("Index out of bound.")
        return self.boxes[x][y]

    def get_king_box(self, is_white) -> (King, Spot):
        empty_box = Spot(0, 0)
        for row in self.boxes:
            for box in row:
                if box.piece is None:
                    continue

                if box.piece.is_white != is_white:
                    continue

                if isinstance(box.piece, King) and box.piece.is_white == is_white:
                    return box.piece, box
        return None, empty_box

    def add_first_rank(self, white) -> None:
        if white:
            i = 0
            self._king_pieces['white'] = Spot(i, 3, King(white))
            king_box = self._king_pieces['white']
        else:
            i = 7
            self._king_pieces['black'] = Spot(i, 3, King(white))
            king_box = self._king_pieces['black']

        row = [Spot(i, 0, Rook(white)),
               Spot(i, 1, Knight(white)),
               Spot(i, 2, Bishop(white)),
               king_box,
               Spot(i, 4, Queen(white)),
               Spot(i, 5, Bishop(white)),
               Spot(i, 6, Knight(white)),
               Spot(i, 7, Rook(white))]

        self.boxes.append(row)

    def add_pawns(self, white) -> None:
        i = 1
        if not white:
            i = 6

        self.boxes.append([Spot(i, j, Pawn(white))
                          for j in range(8)])

    def reset_board(self) -> None:
        """
        Initialize/reset position of black and white pieces
        """
        # Add white pieces
        self.add_first_rank(True)
        self.add_pawns(True)

        # Add empty boxes by marking them as None
        self.boxes.extend([[Spot(i, j, None) for j in range(0, 8)]
                          for i in range(2, 6)])

        # Add black pieces
        self.add_pawns(False)
        self.add_first_rank(False)

    def update_controlled_squares(self) -> None:
        for row in self.boxes:
            for box in row:
                if box.piece is None:
                    continue
                if box.piece.is_white:
                    box.controlled_squares = box.piece.controlled_squares(
                        self, box.x, box.y)
                else:
                    box.controlled_squares = box.piece.controlled_squares(
                        self, box.x, box.y)

    def get_controlled_squares(self, is_white) -> list:
        controlled_squares = []
        for row in self.boxes:
            for box in row:
                if box.piece is None:
                    continue

                if box.piece.is_white and is_white:
                    box.controlled_squares = box.piece.controlled_squares(
                        self, box.x, box.y)
                    controlled_squares.extend(box.controlled_squares)
                elif (not box.piece.is_white) and (not is_white):
                    box.controlled_squares = box.piece.controlled_squares(
                        self, box.x, box.y)
                    controlled_squares.extend(box.controlled_squares)

    @property
    def king_pieces(self) -> dict:
        """Get or set the two Spots where kings are located

        Returns: dict
            {"white": (white king Spot object)
             "black": (black king Spot object)}
        """
        return self._king_pieces

    @king_pieces.setter
    def king_pieces(self, value) -> None:
        if isinstance(value, Spot):
            if value.piece is not None and isinstance(value.piece, King):
                if value.piece.is_white:
                    self._king_pieces['white'] = value
                else:
                    self._king_pieces['black'] = value
            else:
                raise TypeError("piece attribute of Spot must be a King")
        else:
            raise TypeError("value of a key in king_pieces must be a Spot")

    def __str__(self):
        return str([[str(piece) for piece in box] for box in self.boxes])
