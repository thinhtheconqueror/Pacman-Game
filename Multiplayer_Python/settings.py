"""
settings.py

Shared settings for the Multiplayer Pac-Man game.
"""

# Window Settings
WIDTH, HEIGHT = 1920, 1080
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 700, 950
UI_OFFSET_Y = 50
FPS = 60

# Grid Settings
CELL_SIZE = 25 
ROWS = 36
COLS = 28

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # P1 color
GREEN = (0, 255, 0)     # P2 color
RED = (255, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 184, 255)
ORANGE = (255, 184, 82)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (0, 51, 255)
ENERGIZER_COLOR = (255, 204, 204)

ASSETS = {}

# Multiplayer Settings
MAX_PLAYERS = 5  # Maximum players per room (1 Pac-Man + up to 4 Ghosts)
