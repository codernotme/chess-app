import pygame
from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0


    def update_blit(self, surface):
        self.piece.set_texture(size = 120)
        texture = self.piece.texture
        #image
        img = pygame.image.load(texture)
        #rectangle
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)
        #blit
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial = pos[1] // sqsize
        self.initial_col = pos[0] // sqsize

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = None