from color import Color

class Theme:
    def __init__(self, light_bg, dark_bg, light_trace, dark_trace, light_moves, dark_moves):
        # Background colors for light and dark squares
        self.bg = Color(light_bg, dark_bg)
        
        # Trace colors for light and dark piece movement traces
        self.trace = Color(light_trace, dark_trace)
        
        # Move highlight colors for valid moves (light/dark squares)
        self.moves = Color(light_moves, dark_moves)
