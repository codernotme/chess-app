import copy
from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for i in range(cols)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        #move
        piece.moved = True

        #clear valid moves
        piece.clear_moves()
        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(rows):
            for col in range(cols):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False


    def calc_moves(self, piece, row, col, bool=True):
        '''Calculates possible (valid) moves for a given piece at a given position'''
        def pawn_moves():
            steps = 1 if piece.moved else 2
            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))
            for possible_move_row in range (start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        intial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(intial, final)
                        piece.add_move(move)
                    # this means we are blocked
                    else:
                        break
                # this means not in range
                else:
                    break

            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new valid move
                                piece.add_move(move)
                        else:
                            #append new valid move
                            piece.add_move(move)
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1 , col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_moves_row, possible_moves_col = possible_move
                if Square.in_range(possible_moves_row, possible_moves_col):
                    if self.squares[possible_moves_row][possible_moves_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col, final_piece)
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)
        def straightlines_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        #has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    #not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row-0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)

        # castling moves
        if not piece.moved:

            # queen castling
            left_rook = self.squares[row][0].piece
            if isinstance(left_rook, Rook):
                if not left_rook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 3:
                            piece.left_rook = left_rook

                            # rook move
                            initial = Square(row,0)
                            final = Square(row, 3)
                            move = Move(initial, final)
                            left_rook.add_move(move)

                            #king move
                            initial = Square(row,col)
                            final = Square(row, 2)
                            move = Move(initial, final)
                            piece.add_move(move)
            # king castling
            right_rook = self.squares[row][7].piece
            if isinstance(right_rook, Rook):
                if not right_rook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 6:
                            piece.right_rook = right_rook

                            # rook move
                            initial = Square(row,7)
                            final = Square(row, 5)
                            move = Move(initial, final)
                            right_rook.add_move(move)

                            #king move
                            initial = Square(row,col)
                            final = Square(row, 6)
                            move = Move(initial, final)
                            piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightlines_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1) #down-left
            ])
        elif isinstance(piece, Rook):
            straightlines_moves([
                (-1, 0), #up
                (1, 0), #down
                (0, 1), #right
                (0, -1) #left
            ])
        elif isinstance(piece, Queen):
            straightlines_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1), #down-left
                (-1, 0), #up
                (1, 0), #down
                (0, 1), #right
                (0, -1) #left
            ])
        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for r in range (rows):
            for c in range (cols):
                self.squares[r][c] = Square(r, c)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        #All pawns
        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #All Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #All Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))


        #All rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #All Queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #All Kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))