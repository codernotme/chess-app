import pygame

from config import Config
from const import *
from board import Board
from dragger import Dragger
from square import Square

class Game:

    def __init__(self):
        self.next_player = 'black'
        self.board = Board()
        self.dragger = Dragger()
        self.hovered_sqr = None
        self.config = Config()

    # Show methods
    def show_bg(self, surface):
        theme = self.config.theme
        for r in range(rows):
            for c in range (cols):
                color = theme.bg.light if (r+c) % 2 == 0 else theme.bg.dark
                rect = (c*sqsize, r*sqsize, sqsize, sqsize)
                pygame.draw.rect(surface, color, rect)

                #row coordinates
                if c == 0:
                    color = theme.bg.dark if r % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(rows-r),1, color)
                    lbl_pos = (5, 5+r * sqsize)
                    surface.blit(lbl, lbl_pos)
                if r == 7:
                    color = theme.bg.dark if (r+c) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(c),1, color)
                    lbl_pos = (c * sqsize + sqsize - 20, height - 20)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for r in range(rows):
            for c in range(cols):
                if self.board.squares[r][c].has_piece():
                    piece = self.board.squares[r][c].piece

                    #all pieces except
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture)
                        img_center = (c*sqsize + sqsize//2, r*sqsize + sqsize//2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)


    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col*sqsize, move.final.row*sqsize, sqsize, sqsize)
                #blit
                pygame.draw.rect(surface, color, rect)

    def show_last_moves(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in (initial, final):
                #color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                #rect
                rect = (pos.col*sqsize, pos.row*sqsize, sqsize, sqsize)
                #blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = 'gold'
            rect = (self.hovered_sqr.col*sqsize, self.hovered_sqr.row*sqsize, sqsize, sqsize)
            pygame.draw.rect(surface, color, rect, width=3)

# Other Mehtods
    def next_turn(self):
        self.next_player = 'black' if self.next_player == 'white' else 'white'

    def set_hover(self, row, col):
        if 0 <= row < len(self.board.squares) and 0 <= col < len(self.board.squares[row]):
            self.hovered_sqr = self.board.squares[row][col]
        else:
            self.hovered_sqr = None  # Reset hovered_sqr if the indices are out of range


    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()