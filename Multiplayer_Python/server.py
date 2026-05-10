import socket
import threading
import pickle
import pygame
import random
from map_data import load_map_matrix
from entities import Pacman, Ghost
from settings import *

server = "0.0.0.0"
port = 5555

MAX_PLAYERS = 5  # Maximum players in a room

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("=" * 50)
print("    MULTIPLAYER PACMAN SERVER")
print(f"    Max Players: {MAX_PLAYERS}")
print(f"    Rules: 1 Pac-Man, up to {MAX_PLAYERS - 1} Ghosts")
print("=" * 50)
print("Waiting for connections...")

# ── Map Setup ──────────────────────────────────────
grid_matrix = load_map_matrix()
spawn_r, spawn_c = 26, 13
for r in range(ROWS):
    for c in range(COLS):
        if grid_matrix[r][c] == 'P':
            spawn_r, spawn_c = r, c
            grid_matrix[r][c] = ' '

# Ghost spawn positions extracted from map
ghost_spawns = []
for r in range(ROWS):
    for c in range(COLS):
        if grid_matrix[r][c] == 'E':
            ghost_spawns.append((r, c))
            grid_matrix[r][c] = ' '

# AI ghosts (only spawn 2 AI ghosts to leave room for players)
ai_ghosts = []
ai_ghost_colors = [RED, PINK]
# Bỏ sinh ma mặc định để người chơi tự chơi
# for i, (gr, gc) in enumerate(ghost_spawns[:2]):
#     ai_ghosts.append(Ghost(gr, gc, ai_ghost_colors[i % len(ai_ghost_colors)], is_hard_mode=False))

# ── Room State ─────────────────────────────────────
lock = threading.Lock()
player_pacmans = {}   # {player_id: Pacman}  — at most 1 entry
player_ghosts = {}    # {player_id: Ghost}
player_actions = {}   # {player_id: {"dr":0, "dc":0}}
player_connections = {}  # {player_id: conn}
player_names = {}     # {player_id: role_string}

pacman_taken = False   # True when someone is Pac-Man
game_started = False   # True after the Pac-Man player triggers start
game_over = False
total_dots = sum(row.count('0') + row.count('2') for row in grid_matrix)

# Colors for player ghosts
ghost_player_colors = [ORANGE, CYAN, (180, 80, 255), (255, 120, 120)]

def get_player_count():
    return len(player_pacmans) + len(player_ghosts)

def get_room_info():
    """Build room info dict to send to clients."""
    players = []
    for pid in player_pacmans:
        players.append({"id": pid, "role": "pacman"})
    for pid in player_ghosts:
        players.append({"id": pid, "role": "ghost"})
    return {
        "type": "room_info",
        "players": players,
        "pacman_taken": pacman_taken,
        "player_count": get_player_count(),
        "max_players": MAX_PLAYERS,
        "game_started": game_started,
    }

def broadcast_room_info():
    """Send updated room info to all connected players."""
    info = get_room_info()
    data = pickle.dumps(info)
    for pid, conn in list(player_connections.items()):
        try:
            conn.sendall(data)
        except:
            pass

# ── Game Loop ──────────────────────────────────────
pending_sounds = []  # Sound events to send to clients
pending_effects = [] # Visual effects like score popups

def game_loop():
    global game_over, total_dots
    clock = pygame.time.Clock()
    while True:
        with lock:
            if not game_started or game_over:
                clock.tick(FPS)
                continue
            
            # Clear events from previous tick
            pending_sounds.clear()
            pending_effects.clear()

            # Update player Pac-Mans
            for pid, p in list(player_pacmans.items()):
                if pid in player_actions:
                    p.set_direction(player_actions[pid]["dr"], player_actions[pid]["dc"])
                p.update(grid_matrix)

            # Update player ghosts
            for pid, g in list(player_ghosts.items()):
                if g.is_dead:
                    g.respawn_timer -= 1
                    if g.respawn_timer <= 0:
                        g.is_dead = False
                        g.r, g.c = g.start_r, g.start_c
                    continue

                if not hasattr(g, "p_move_timer"):
                    g.p_move_timer = 0

                # Frightened ghosts move slower
                delay = 30 if g.frightened_timer > 0 else 15

                if g.frightened_timer > 0:
                    g.frightened_timer -= 1

                g.p_move_timer += 1
                if g.p_move_timer >= delay:
                    g.p_move_timer = 0
                    if pid in player_actions:
                        action = player_actions[pid]
                        # Try the queued action first
                        n_r = g.r + action["dr"]
                        n_c = g.c + action["dc"]
                        
                        if n_c < 0: n_c = COLS - 1
                        elif n_c >= COLS: n_c = 0
                        
                        if 0 <= n_r < ROWS and 0 <= n_c < COLS and grid_matrix[n_r][n_c] != '1':
                            g.r = n_r
                            g.c = n_c
                            g.dr = action["dr"]
                            g.dc = action["dc"]
                        else:
                            # If queued action is blocked, continue in the current direction
                            curr_r = g.r + g.dr
                            curr_c = g.c + g.dc
                            
                            if curr_c < 0: curr_c = COLS - 1
                            elif curr_c >= COLS: curr_c = 0
                            
                            if 0 <= curr_r < ROWS and 0 <= curr_c < COLS and grid_matrix[curr_r][curr_c] != '1':
                                g.r = curr_r
                                g.c = curr_c
                            else:
                                g.dr = 0
                                g.dc = 0

            # Dots logic
            for pid, p in list(player_pacmans.items()):
                res = p.check_eat_dot(grid_matrix)
                if res == 'ENERGIZER':
                    total_dots -= 1
                    pending_sounds.append('energizer')
                    pending_effects.append({"type": "energizer", "r": p.r, "c": p.c})
                    for g in ai_ghosts:
                        g.frighten()
                    for pgid, pg in player_ghosts.items():
                        pg.frighten()
                elif res == 'DOT':
                    total_dots -= 1
                    pending_sounds.append('eat')
                    pending_effects.append({"type": "dot", "r": p.r, "c": p.c})
            
            if total_dots <= 0:
                game_over = True
                
            # AI ghosts logic
            for g in ai_ghosts:
                target = None
                min_d = 9999
                for pid, p in player_pacmans.items():
                    d = abs(g.r - p.r) + abs(g.c - p.c)
                    if d < min_d:
                        min_d = d
                        target = p
                if target:
                    g.update(target, grid_matrix, ai_ghosts + list(player_ghosts.values()))
                else:
                    g.update(Pacman(1,1), grid_matrix, ai_ghosts)

            # Collision logic
            all_ghosts = ai_ghosts + list(player_ghosts.values())
            for pid, p in list(player_pacmans.items()):
                for g in all_ghosts:
                    if g.r == p.r and g.c == p.c:
                        if g.frightened_timer > 0 and not g.is_dead:
                            g.die()
                            # Don't set respawn_timer here — let entity.update()
                            # BFS the ghost back to spawn first
                            p.score += 200
                            pending_sounds.append('ghost')
                            pending_effects.append({"type": "ghost", "r": g.r, "c": g.c})
                        elif not g.is_dead:
                            p.lives -= 1
                            pending_sounds.append('death')
                            if p.lives <= 0:
                                game_over = True
                            else:
                                p.r, p.c = p.start_r, p.start_c
                                for bg in all_ghosts:
                                    bg.r, bg.c = bg.start_r, bg.start_c
                                    bg.is_dead = False
                                    bg.frightened_timer = 0
                                    if hasattr(bg, 'respawn_timer'):
                                        bg.respawn_timer = 0

        clock.tick(FPS)

threading.Thread(target=game_loop, daemon=True).start()

current_player = 0

def build_game_state():
    """Build the game state dict to send to clients."""
    return {
        "type": "game_state",
        "pacmans": [
            {
                "r": p.r, "c": p.c, "score": p.score, "lives": p.lives,
                "dr": p.dr, "dc": p.dc, "color": p.color, "pid": pid
            }
            for pid, p in player_pacmans.items()
        ],
        "ghosts": [
            {
                "r": g.r, "c": g.c, "color": g.color,
                "frightened": g.frightened_timer > 0,
                "dead": g.is_dead, "dr": g.dr, "dc": g.dc,
                "is_player": False
            }
            for g in ai_ghosts
        ] + [
            {
                "r": g.r, "c": g.c, "color": g.color,
                "frightened": g.frightened_timer > 0,
                "dead": g.is_dead, "dr": g.dr, "dc": g.dc,
                "is_player": True, "pid": pid
            }
            for pid, g in player_ghosts.items()
        ],
        "grid": grid_matrix,
        "player_count": get_player_count(),
        "pacman_taken": pacman_taken,
        "game_started": game_started,
        "game_over": game_over,
        "sounds": list(pending_sounds),
        "effects": list(pending_effects),
    }

def threaded_client(conn, player):
    global current_player, pacman_taken, game_started

    # Send player ID
    conn.send(str.encode(str(player)))

    # Wait for init data (role request)
    try:
        init_data = pickle.loads(conn.recv(4096))
        requested_role = init_data.get("role", "ghost")
    except:
        conn.close()
        return

    with lock:
        # Enforce max player limit
        if get_player_count() >= MAX_PLAYERS:
            try:
                conn.sendall(pickle.dumps({
                    "type": "error",
                    "message": "Room is full! Max {} players.".format(MAX_PLAYERS)
                }))
            except:
                pass
            conn.close()
            return

        # Enforce 1 Pac-Man rule
        assigned_role = requested_role
        if requested_role == "pacman":
            if pacman_taken:
                # Pac-Man slot already taken → force to ghost
                assigned_role = "ghost"
            else:
                pacman_taken = True

        # Send role assignment confirmation
        ghost_idx = len(player_ghosts)
        try:
            conn.sendall(pickle.dumps({
                "type": "role_assigned",
                "role": assigned_role,
                "requested": requested_role,
                "player_id": player,
                "player_count": get_player_count() + 1,
                "max_players": MAX_PLAYERS,
            }))
        except:
            conn.close()
            return

        player_actions[player] = {"dr": 0, "dc": 0}
        player_connections[player] = conn
        player_names[player] = assigned_role

        if assigned_role == "pacman":
            p = Pacman(spawn_r, spawn_c)
            p.color = YELLOW
            player_pacmans[player] = p
            print(f"[PLAYER {player}] Joined as PAC-MAN ★")
        else:
            # Find a ghost spawn position
            if ghost_spawns:
                gr, gc = ghost_spawns[ghost_idx % len(ghost_spawns)]
            else:
                gr, gc = spawn_r - 3, spawn_c
            g = Ghost(gr, gc, ghost_player_colors[ghost_idx % len(ghost_player_colors)], is_hard_mode=False)
            player_ghosts[player] = g
            print(f"[PLAYER {player}] Joined as GHOST 👻")

        print(f"  → Room: {get_player_count()}/{MAX_PLAYERS} players | Pac-Man taken: {pacman_taken}")

    # Main communication loop
    while True:
        try:
            raw = conn.recv(4096)
            if not raw:
                break

            data = pickle.loads(raw)

            with lock:
                # Handle special commands
                if isinstance(data, dict) and data.get("type") == "start_game":
                    if not game_started:
                        game_started = True
                        print("[SERVER] Game started!")
                    # Send back current state
                    conn.sendall(pickle.dumps(build_game_state()))
                    continue

                # Regular movement action
                player_actions[player] = data

                # Send game state back
                conn.sendall(pickle.dumps(build_game_state()))

        except Exception as e:
            break

    # Cleanup on disconnect
    with lock:
        print(f"[PLAYER {player}] Disconnected ({player_names.get(player, '?')})")
        if player in player_pacmans:
            del player_pacmans[player]
            pacman_taken = False
            print("  → Pac-Man slot is now FREE")
        if player in player_ghosts:
            del player_ghosts[player]
        if player in player_actions:
            del player_actions[player]
        if player in player_connections:
            del player_connections[player]
        if player in player_names:
            del player_names[player]
        print(f"  → Room: {get_player_count()}/{MAX_PLAYERS} players")

    conn.close()

while True:
    conn, addr = s.accept()
    with lock:
        if get_player_count() >= MAX_PLAYERS:
            print(f"Rejected connection from {addr} — room is full!")
            try:
                conn.send(str.encode("-1"))
            except:
                pass
            conn.close()
            continue

    print(f"Connection from: {addr}")
    threading.Thread(target=threaded_client, args=(conn, current_player)).start()
    current_player += 1
