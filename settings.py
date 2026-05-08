"""
settings.py

This module contains global constants and configurations for the Pacman DSA project.
It defines window dimensions, grid sizes, and color palettes used throughout the application.
"""

# Window Settings
WIDTH, HEIGHT = 1920, 1080
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 700, 950
UI_OFFSET_Y = 50
FPS = 60

# Grid Settings
# Apply the DSA concept: we divide the visual space into a discrete Grid (2D Matrix array)
CELL_SIZE = 25 
ROWS = 36
COLS = 28

# Colors (Global constants for UI elements)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Pacman color
RED = (255, 0, 0)       # Blinky color
CYAN = (0, 255, 255)    # Inky color
PINK = (255, 184, 255)  # Pinky color
ORANGE = (255, 184, 82) # Clyde color
BLUE = (0, 0, 255)      # Wall color
GRAY = (128, 128, 128)  # Dot/Coin color
LIGHT_BLUE = (0, 51, 255)# Frightened ghost color
ENERGIZER_COLOR = (255, 204, 204) # Energizer color
ASSETS = {}
