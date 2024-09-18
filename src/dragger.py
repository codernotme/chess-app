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
        if self.piece:
            # Set the texture size for dragging
            self.piece.set_texture(size=120)
            texture = self.piece.texture
            # Load the image
            img = pygame.image.load(texture)
            # Get the rectangle for the image
            img_center = (self.mouseX, self.mouseY)
            self.piece.texture_rect = img.get_rect(center=img_center)
            # Blit the image to the surface
            surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, pos):
        """Update the mouse coordinates."""
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        """Save the initial position when dragging starts."""
        self.initial_row = pos[1] // sqsize
        self.initial_col = pos[0] // sqsize

    def drag_piece(self, piece):
        """Begin dragging the piece."""
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        """Stop dragging and reset the piece."""
        self.piece = None
        self.dragging = False
