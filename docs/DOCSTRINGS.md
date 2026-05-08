# 📚 API & Docstrings Reference

Tài liệu này tổng hợp các docstring quan trọng nhất của các class, module và functions cốt lõi được sử dụng trong dự án Pac-Man.

---

## 1. Thuật toán Trí Tuệ Nhân Tạo (AI) - `algorithms.py`

### `bfs_shortest_path(start, target, grid, occupied_positions)`
```python
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
```

### `random_walk_algorithm(start, grid, occupied_positions)`
```python
"""
EASY DIFFICULTY AI / BFS FALLBACK:
Logic: Random selection of valid neighbors.

This algorithm picks a random valid direction at each step.
In demo_tuan2.py, it only activates as fallback when BFS
cannot find a path to the target (target fully enclosed).

Args:
    start (tuple): The current (row, col) position of the ghost.
    grid (list[list[str]]): The 2D grid matrix.
    occupied_positions (set, optional): Positions of other ghosts.
    
Returns:
    tuple: The next (row, col) position to move to.
    
Complexity:
    Time: O(1)
"""
```

### `get_valid_neighbors(pos, grid, occupied_positions)`
```python
"""
Finds all navigable adjacent cells (Up, Down, Left, Right) from a given position.

A cell is considered navigable if it is within grid boundaries, not a wall ('1'),
and not currently occupied by another entity. Includes Tunnel Wrap Around logic.

Args:
    pos (tuple): The current (row, col) position.
    grid (list[list[str]]): The 2D grid matrix.
    occupied_positions (set, optional): Positions of other ghosts to avoid collision.
    
Returns:
    list[tuple]: A list of navigable (row, col) neighbor positions.
    
Complexity:
    Time: O(1) - Constant time as it only checks 4 directions.
"""
```

---

## 2. Thực thể trò chơi (Entities) - `entities.py`

### `frighten()`
```python
"""
Activates frightened mode for a ghost.
During this state, the ghost becomes vulnerable, moves slower,
changes its visual appearance and can be eaten by Pac-Man.
"""
```

---

## 3. Hệ thống Game Loop và Giao diện - `main.py`

### `main_menu()`
```python
"""
Displays the splash screen and difficulty selection menu.
Allows the player to choose game difficulty and number of ghosts
before entering the main game loop.
"""
```

### `game_loop()`
```python
"""
Runs the main offline Pac-Man gameplay loop.
Handles player input, entity updates, collision checks, scoring,
audio events, visual effects, win/lose states and rendering.
"""
```

### `create_wall_surface()`
```python
"""
Creates a static glowing surface for the map walls.
Draws wall connections with layered alpha lines to create
a neon glow effect while avoiding redrawing expensive wall
effects from scratch every frame.
"""
```

### `draw_synthwave_bg()`
```python
"""
Draws a moving synthwave grid background.
Uses time-based offsets to animate horizontal grid lines and
create a retro arcade visual style behind the map.
"""
```

---

## 4. Hệ thống Mạng Đa Người Chơi (Multiplayer)

### Class `Network` (`Multiplayer_Python/network.py`)
```python
"""
Client-side networking helper.
Connects to the game server, sends role selection and player input,
then receives the latest serialized game state from the server.
"""
```

### `build_game_state()` (`Multiplayer_Python/server.py`)
```python
"""
Builds the authoritative game state dictionary on the server.
The state includes map data, Pac-Man players, Ghost players,
AI ghosts, score, room status and sound events for clients.
"""
```
