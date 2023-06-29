from pieces import Piece, Queen, Rook, Bishop, Knight

piece_classes: dict[str, type[Piece]] = {
    'Queen': Queen,
    'Rook': Rook,
    'Bishop': Bishop,
    'Knight': Knight
}
"""
A dictionary mapping the names of chess piece types to their respective classes.

The keys represent the names of the chess pieces as strings, and the values are references
to the corresponding class objects for each piece type.

Example usage:
```
QueenPiece = piece_classes['Queen']
queen = QueenPiece(...)
```
"""
