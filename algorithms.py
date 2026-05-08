"""
algorithms.py

This module implements the core Data Structures and Algorithms (DSA) for ghost AI.
It includes graph traversal algorithms for pathfinding in the game grid.
"""

import collections
import random

def get_valid_neighbors(pos, grid, occupied_positions=None):
    """
    Finds all navigable adjacent cells (Up, Down, Left, Right) from a given position.
    
    A cell is considered navigable if it is within grid boundaries, not a wall ('1'),
    and not currently occupied by another entity.
    
    Args:
        pos (tuple): The current (row, col) position.
        grid (list[list[str]]): The 2D grid matrix.
        occupied_positions (set, optional): Positions of other ghosts to avoid collision.
        
    Returns:
        list[tuple]: A list of navigable (row, col) neighbor positions.
        
    Complexity:
        Time: O(1) - Constant time as it only checks 4 directions.
    """
    if occupied_positions is None:
        occupied_positions = set()
        
    r, c = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        
        # Tunnel wrap around logic
        if nc < 0:
            nc = len(grid[0]) - 1
        elif nc >= len(grid[0]):
            nc = 0
            
        # Boundary checks inside grid graph array
        if 0 <= nr < len(grid):
            if grid[nr][nc] != '1' and (nr, nc) not in occupied_positions:  # Not a wall and not occupied by another ghost
                neighbors.append((nr, nc))
    return neighbors


def random_walk_algorithm(start, grid, occupied_positions=None):
    """
    EASY DIFFICULTY AI:
    Logic: Random selection of valid neighbors.
    
    This algorithm simulates basic or "confused" ghost behavior by picking
    a random valid direction at each step.
    
    Args:
        start (tuple): The current (row, col) position of the ghost.
        grid (list[list[str]]): The 2D grid matrix.
        occupied_positions (set, optional): Positions of other ghosts.
        
    Returns:
        tuple: The next (row, col) position to move to.
        
    Complexity:
        Time: O(1)
    """
    neighbors = get_valid_neighbors(start, grid, occupied_positions)
    if not neighbors:
        return start # Trapped
    return random.choice(neighbors)


def bfs_shortest_path(start, target, grid, occupied_positions=None):
    """
    HARD DIFFICULTY AI (Breadth-First Search):
    Logic: Level-order traversal to find the shortest path in an unweighted graph.
    
    Guarantees the absolute shortest path to the target (Pacman) by exploring
    all possible paths level-by-level using a Queue.
    
    Data Structures: 
    - Queue (collections.deque): For O(1) enqueue/dequeue operations.
    - Dictionary (parent_map): To track visited nodes and reconstruct the path.
    
    Args:
        start (tuple): The starting (row, col) position.
        target (tuple): The target (row, col) position (usually Pacman).
        grid (list[list[str]]): The 2D grid matrix.
        occupied_positions (set, optional): Positions of other ghosts.
        
    Returns:
        tuple: The immediate next (row, col) position on the shortest path.
        
    Complexity:
        Time: O(V + E) where V is the number of grid cells and E is the number of valid moves.
        Space: O(V) to store the visited nodes in the parent_map and queue.
    """
    # 1. Base cases
    if start == target:
        return start
    
    # 2. Queue for BFS: stores (current_node)
    queue = collections.deque([start])
    
    # 3. Visited tracking & Path reconstruction (node : parent_node)
    parent_map = {start: None}
    
    path_found = False
    
    while queue:
        current = queue.popleft()
  
        if current == target:
            path_found = True
            break
            
        # Explore neighbors
        for neighbor in get_valid_neighbors(current, grid, occupied_positions):
            if neighbor not in parent_map: # Unvisited node
                parent_map[neighbor] = current
                queue.append(neighbor)
                
    # 4. If target found, backtrack from target to start using parent_map
    if path_found:
        curr = target
        path = []
        while curr != start:
            path.append(curr)
            curr = parent_map[curr]
            
        path.reverse() # Reverse to get path from start -> target
        
        # Return the *next immediate step* the ghost must take
        if len(path) > 0:
            return path[0] 
            
    # Fallback to random walk if target is fully enclosed/unreachable
    return random_walk_algorithm(start, grid, occupied_positions)
