"""
map_data.py

This module defines the static map layout for the Pacman game.
In term of Data Structures and Algorithms (DSA), the grid is treated as an unweighted Graph
where each cell is a node and adjacency represents edges for movement.

Grid Legend:
1 = Wall
0 = Dot (Coin)
P = Pacman Starting Position
E = Ghost Starting Position
' ' = Empty walkable space
"""

GAME_MAP = [
    "1111111111111111111111111111",
    "1111111111111111111111111111",
    "1111111111111111111111111111",
    "1111111111111111111111111111",
    "1000000000000110000000000001",
    "1011110111110110111110111101",
    "1211110111110110111110111121",
    "1011110111110110111110111101",
    "1000000000000000000000000001",
    "1011110110111111110110111101",
    "1011110110111111110110111101",
    "1000000110000110000110000001",
    "111111011111 11 111110111111",
    "      011111 11 111110      ",
    "      011             11      ",
    "      011 111DD111 11      ",
    "111111011 1      1 110111111",
    "      0   1  EE  1   0      ",
    "111111011 1      1 110111111",
    "      011 11111111 11      ",
    "      011          11      ",
    "      011 11111111 11      ",
    "111111011 11111111 110111111",
    "1000000000000110000000000001",
    "1011110111110110111110111101",
    "1011110111110110111110111101",
    "1200110000000  0000000110021",
    "1110110110111111110110110111",
    "1110110110111111110110110111",
    "1000000110000110000110000001",
    "1011111111110110111111111101",
    "1011111111110110111111111101",
    "1000000000000000000000000001",
    "1111111111111111111111111111",
    "1111111111111111111111111111",
    "1111111111111111111111111111"
]

def load_map_matrix():
    """
    Returns the classic 28x36 arcade maze map as a 2D list.
    """
    grid = []
    for row in GAME_MAP:
        # Pad with space if string is too short (just in case)
        row = row.ljust(28, ' ')
        grid.append(list(row))
        
    # Place Pacman spawn randomly in a central path (row 26, col 13 or 14)
    grid[26][13] = 'P'
    
    return grid