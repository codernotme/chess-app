import pygame
import os
from sound import Sound
from theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav')
        )
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav')
        )

    def change_theme(self):
        # Cycle through themes when called
        self.idx = (self.idx + 1) % len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        # Enhanced themes with vibrant color palettes

        green = Theme(
            (234, 235, 200),  # Light green square
            (119, 154, 88),   # Dark green square
            (244, 247, 116),  # Bright yellow highlight
            (172, 195, 51),   # Olive green highlight
            '#A86464',        # Soft red capture light
            '#904646'         # Deep red capture dark
        )

        brown = Theme(
            (238, 217, 181),  # Soft beige square
            (181, 136, 99),   # Warm brown square
            (255, 235, 156),  # Golden highlight
            (196, 156, 85),   # Rich amber highlight
            '#B86464',        # Muted red capture light
            '#964646'         # Rich red capture dark
        )

        blue = Theme(
            (212, 227, 255),  # Sky blue square
            (95, 140, 170),   # Deep ocean blue square
            (173, 216, 230),  # Light aqua highlight
            (67, 138, 179),   # Bright blue highlight
            '#8A6464',        # Subtle pink capture light
            '#764646'         # Burgundy capture dark
        )

        gray = Theme(
            (200, 200, 200),  # Light gray square
            (100, 100, 100),  # Dark charcoal square
            (160, 160, 160),  # Silver highlight
            (80, 80, 80),     # Slate gray highlight
            '#706464',        # Desaturated capture light
            '#604646'         # Dark rust capture dark
        )

        self.themes = [green, brown, blue, gray]
