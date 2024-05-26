import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Chess Game')
        self.game = Game()
    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            # show methods
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            if dragger.dragging:
                dragger.update_blit(screen)

            for i in pygame.event.get():
                #click
                if i.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(i.pos)
                    clicked_col = dragger.mouseX // sqsize
                    clicked_row = dragger.mouseY // sqsize
                    if  board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(i.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                #mouse motion
                elif i.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(i.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)


                #click release
                elif i.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(i.pos)
                        released_col = dragger.mouseX // sqsize
                        released_row = dragger.mouseY // sqsize

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        # is it a valid move?
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            # show methods
                            game.show_bg(screen)
                            game.show_pieces(screen)
                    dragger.undrag_piece()

                #quit application
                elif i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.mainloop()