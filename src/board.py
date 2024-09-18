from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        # Initialize an 8x8 board with empty squares
        self.squares = [[Square(row, col) for col in range(cols)] for row in range(rows)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        # Update the board with the move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Move the piece
        piece.moved = True

        # Clear valid moves for the piece
        piece.clear_moves()

        # Set the last move
        self.last_move = move

    def valid_move(self, piece, move):
        # Check if a move is valid based on the piece's possible moves
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        '''Calculates possible (valid) moves for a given piece at a given position'''
        def pawn_moves():
            steps = 1 if piece.moved else 2
            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    # Blocked by another piece
                    else:
                        break
                else:
                    break

            # Diagonal moves (captures)
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            # 8 possible knight moves
            possible_moves = [
                (row - 2, col + 1), (row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1),
                (row + 2, col - 1), (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightlines_moves(incrs):
            # Moving along straight lines (Rook, Bishop, Queen)
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        # Empty square
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)
                        # Capture enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        # Blocked by team piece
                        else:
                            break
                    else:
                        break

                    # Increment row and col for further moves
                    possible_move_row += row_incr
                    possible_move_col += col_incr

        def king_moves():
            # 8 possible adjacent squares for king
            adjs = [
                (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1),
                (row + 1, col), (row + 1, col - 1), (row, col - 1), (row - 1, col - 1)
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightlines_moves([(-1, 1), (-1, -1), (1, 1), (1, -1)])  # Diagonal moves
        elif isinstance(piece, Rook):
            straightlines_moves([(-1, 0), (1, 0), (0, 1), (0, -1)])  # Vertical and horizontal moves
        elif isinstance(piece, Queen):
            straightlines_moves([(-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)])  # All directions
        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        # Initialize each square on the board
        for r in range(rows):
            for c in range(cols):
                self.squares[r][c] = Square(r, c)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Add pawns
        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Add knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Add bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Add rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Add queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # Add kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))
