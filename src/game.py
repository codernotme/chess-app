import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # Show methods
    def show_bg(self, surface):
        for r in range(rows):
            for c in range (cols):
                if (r+c) % 2 == 0:
                    color = (234, 235, 201)
                else:
                    color = (119, 154, 88)
                rect = (c*sqsize, r*sqsize, sqsize, sqsize)
                pygame.draw.rect(surface, color, rect)

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
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                #color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                #rect
                rect = (move.final.col*sqsize, move.final.row*sqsize, sqsize, sqsize)
                #blit
                pygame.draw.rect(surface, color, rect)