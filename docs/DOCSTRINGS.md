# 📚 API Documentation & Game Logic (Docstrings)

This document provides a detailed explanation of the functions, parameters, and time complexities of the core algorithms and systems used in the Pac-Man DSA Project (including AI and Multiplayer components).

---

## 1. Artificial Intelligence (AI) - `algorithms.py`

### 🔹 `bfs_shortest_path(start, target, grid, occupied_positions)`
**Description:** Breadth-First Search (BFS) algorithm. Used as the Hard difficulty AI. Guarantees finding the absolute shortest path for the Ghosts to reach Pac-Man.
* **Logic:** Performs a level-order traversal on the unweighted graph (2D grid). Utilizes a Queue for constant time `O(1)` enqueue/dequeue operations and a Dictionary to track visited nodes and reconstruct the path.
* **Parameters:**
  * `start` *(tuple)*: The `(row, col)` starting position of the Ghost.
  * `target` *(tuple)*: The `(row, col)` target position (usually Pac-Man's location).
  * `grid` *(list[list[str]])*: The 2D matrix representing the maze.
  * `occupied_positions` *(set, optional)*: A set of positions currently occupied by other Ghosts (prevents entities from overlapping).
* **Returns:** `tuple` - The `(row, col)` coordinate of the next optimal step.
* **Complexity:** Time `O(V + E)`, Space `O(V)`. (Where V is the number of vertices/cells and E is the number of valid edges/moves).

### 🔹 `random_walk_algorithm(start, grid, occupied_positions)`
**Description:** Random walk algorithm. Used as the Easy difficulty AI or as a fallback when the BFS target is unreachable.
* **Logic:** Retrieves all valid adjacent cells (not blocked by walls) and randomly selects a direction to move.
* **Parameters:** Same as the BFS function.
* **Returns:** `tuple` - The coordinate of the next random step.
* **Complexity:** Time `O(1)`.

### 🔹 `get_valid_neighbors(pos, grid, occupied_positions)`
**Description:** Auxiliary function that finds all navigable adjacent cells (Up, Down, Left, Right) from a given coordinate.
* **Logic:** Ignores wall cells (`'1'`), out-of-bound cells, and cells already occupied by another Ghost. Integrates the tunnel wrap-around mechanic.
* **Returns:** `list[tuple]` - A list of valid neighboring coordinates.

---

## 2. Entity System - `entities.py`

### 🔹 `Ghost.frighten()`
**Description:** Activates the Frightened Mode for the ghost when Pac-Man consumes an Energizer.
* **Effects:** 
  * The ghost's appearance changes (turns dark blue and flashes white/red before ending).
  * Movement speed is significantly reduced.
  * The AI pathfinding algorithm is temporarily altered (switches to random walk).
  * Pac-Man can chase and "eat" the ghost for bonus points.

---

## 3. Game Loop - `main.py` & `app.py`

### 🔹 `main_menu()`
**Description:** Displays the offline game's splash screen and difficulty selection menu.
* **Functionality:** Allows the player to choose the AI difficulty (Easy/Hard) and customize the number of Ghosts appearing on the map before starting the offline game.

### 🔹 `game_loop()`
**Description:** The core lifecycle loop of the offline game mode.
* **Functionality:** Handles continuous frame-by-frame logic (60 FPS): receives player input, updates entity positions, handles collision detection (eating dots, eating ghosts, getting caught), manages the score, triggers audio events, and renders graphics to the screen.

### 🔹 `create_wall_surface()`
**Description:** Initializes the static graphical surface for the maze.
* **Functionality:** Draws transparent overlapping lines to create a neon glow effect for the walls. This function is only executed once during initialization to optimize the frame rate, avoiding the need to redraw complex wall graphics every frame.

---

## 4. Multiplayer Network - `Multiplayer_Python/`

### 🔹 Class `Network` (`network.py`)
**Description:** Object that manages the socket connection from the Client side.
* **Functionality:** Establishes and maintains a TCP connection to the Server, continuously sending player control inputs (keystrokes) and receiving the latest authoritative GameState, serialized using Python's `pickle`.

### 🔹 `build_game_state()` (`server.py`)
**Description:** Packages the entire synchronized room state on the Server.
* **Functionality:** Collects real-time position data of all players (Pac-Man and Ghosts), AI ghost paths, current scores, remaining map dots, and audio/visual events (sirens, eat sounds, popups)... compiling them into a complete `Dictionary` to be broadcasted to all connected Clients to ensure synchronization and prevent lag.
