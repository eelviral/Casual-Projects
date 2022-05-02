from spot import Spot
from pieces import *


class Board:
    def __init__(self):
        self.boxes = []
        self.white_top_spawn = False

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

    def add_first_rank(self, white, rank) -> None:
        row = [Spot(rank, 0, Rook(white)),
               Spot(rank, 1, Knight(white)),
               Spot(rank, 2, Bishop(white))]
        if (rank == 0 and white) or (rank == 7 and not white):
            row += [Spot(rank, 3, King(white)),
                    Spot(rank, 4, Queen(white))]
        elif (rank == 0 and not white) or (rank == 7 and white):
            row += [Spot(rank, 3, Queen(white)),
                    Spot(rank, 4, King(white))]
        row += [Spot(rank, 5, Bishop(white)),
                Spot(rank, 6, Knight(white)),
                Spot(rank, 7, Rook(white))]

        self.boxes.append(row)

    def add_pawns(self, white, rank) -> None:
        if rank == 1:
            white_top_spawn = True
        else:
            white_top_spawn = False
        self.boxes.append([Spot(rank, j, Pawn(white, white_top_spawn))
                          for j in range(8)])

    def reset_board(self) -> None:
        """
        Initialize/reset position of black and white pieces
        """
        if self.white_top_spawn:
            self.add_first_rank(True, 0)
            self.add_pawns(True, 1)
        else:
            self.add_first_rank(False, 0)
            self.add_pawns(False, 1)

        # Add empty boxes by marking them as None
        self.boxes.extend([[Spot(i, j, None) for j in range(0, 8)]
                          for i in range(2, 6)])

        if self.white_top_spawn:
            self.add_pawns(False, 6)
            self.add_first_rank(False, 7)
        else:
            self.add_pawns(True, 6)
            self.add_first_rank(True, 7)

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

        return list(set(controlled_squares))

    def __repr__(self):
        return '\n'.join(map(repr, [[repr(spot) for spot in box] for box in self.boxes]))

    def __str__(self):
        return '\n'.join(map(str, [[str(spot) for spot in box] for box in self.boxes]))
