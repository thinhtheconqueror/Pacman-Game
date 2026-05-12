"""
client.py

Handles the multiplayer client-side logic, rendering the game state received from the server.
"""
import pygame
import pygame.gfxdraw
import sys
import math
from settings import *
from network import Network
from entities import Pacman, Ghost
from map_data import load_map_matrix

def create_wall_surface(grid):
    """Generates the static glowing neon wall surface for the multiplayer map."""
    surf = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
    pad = 8
    
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == '1':
                x = col * CELL_SIZE
                y = row * CELL_SIZE + UI_OFFSET_Y
                
                is_top = (row > 0 and grid[row-1][col] == '1') or (row == 0)
                is_bottom = (row < ROWS - 1 and grid[row+1][col] == '1') or (row == ROWS - 1)
                is_left = (col > 0 and grid[row][col-1] == '1') or (col == 0)
                is_right = (col < COLS - 1 and grid[row][col+1] == '1') or (col == COLS - 1)
                
                lines = []
                if not is_top: lines.append(((x, y + pad), (x + CELL_SIZE, y + pad)))
                if not is_bottom: lines.append(((x, y + CELL_SIZE - pad), (x + CELL_SIZE, y + CELL_SIZE - pad)))
                if not is_left: lines.append(((x + pad, y), (x + pad, y + CELL_SIZE)))
                if not is_right: lines.append(((x + CELL_SIZE - pad, y), (x + CELL_SIZE - pad, y + CELL_SIZE)))
                    
                if is_top and is_left and (row > 0 and col > 0 and grid[row-1][col-1] != '1'):
                    lines.append(((x, y + pad), (x + pad, y + pad)))
                    lines.append(((x + pad, y), (x + pad, y + pad)))
                if is_top and is_right and (row > 0 and col < COLS - 1 and grid[row-1][col+1] != '1'):
                    lines.append(((x + CELL_SIZE - pad, y + pad), (x + CELL_SIZE, y + pad)))
                    lines.append(((x + CELL_SIZE - pad, y), (x + CELL_SIZE - pad, y + pad)))
                if is_bottom and is_left and (row < ROWS - 1 and col > 0 and grid[row+1][col-1] != '1'):
                    lines.append(((x, y + CELL_SIZE - pad), (x + pad, y + CELL_SIZE - pad)))
                    lines.append(((x + pad, y + CELL_SIZE - pad), (x + pad, y + CELL_SIZE)))
                if is_bottom and is_right and (row < ROWS - 1 and col < COLS - 1 and grid[row+1][col+1] != '1'):
                    lines.append(((x + CELL_SIZE - pad, y + CELL_SIZE - pad), (x + CELL_SIZE, y + CELL_SIZE - pad)))
                    lines.append(((x + CELL_SIZE - pad, y + CELL_SIZE - pad), (x + CELL_SIZE - pad, y + CELL_SIZE)))

                wall_c = (0, 255, 255) # Cyan neon
                for p1, p2 in lines:
                    pygame.draw.line(surf, (*wall_c, 30), p1, p2, 12)
                    pygame.draw.line(surf, (*wall_c, 80), p1, p2, 6)
                    pygame.draw.aaline(surf, (255, 255, 255, 255), p1, p2)
                    
                    pygame.draw.circle(surf, (*wall_c, 30), p1, 6)
                    pygame.draw.circle(surf, (*wall_c, 30), p2, 6)
                    pygame.draw.circle(surf, (*wall_c, 80), p1, 3)
                    pygame.draw.circle(surf, (*wall_c, 80), p2, 3)
                    pygame.draw.circle(surf, (255, 255, 255, 255), p1, 1)
                    pygame.draw.circle(surf, (255, 255, 255, 255), p2, 1)
    return surf

def draw_items(surface, grid):
    """Draws consumable items (dots and energizers) on the given surface."""
    time_ms = pygame.time.get_ticks()
    pulse = (math.sin(time_ms * 0.005) + 1) / 2
    
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            if val in ('0', '2'):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + UI_OFFSET_Y
                cx = x + CELL_SIZE // 2
                cy = y + CELL_SIZE // 2
                
                if val == '0':
                    dot_r = 2 + pulse * 1.5
                    dot_c = (255, 50, 150)
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(dot_r + 4), (*dot_c, 50))
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(dot_r), dot_c)
                elif val == '2':
                    eng_r = 6 + pulse * 3
                    eng_c = (255, 255, 50)
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(eng_r + 6), (*eng_c, 80))
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(eng_r), eng_c)

def draw_synthwave_bg(surface):
    """Draws a moving 2026 outrun / synthwave grid background."""
    time_ms = pygame.time.get_ticks()
    surface.fill((10, 0, 20, 255))
    offset = (time_ms * 0.05) % CELL_SIZE
    grid_color = (40, 10, 80, 255)
    
    for c in range(0, COLS + 1):
        x = c * CELL_SIZE
        pygame.draw.line(surface, grid_color, (x, 0), (x, VIRTUAL_HEIGHT), 1)
        
    for r in range(-1, ROWS + 1):
        y = r * CELL_SIZE + offset
        pygame.draw.line(surface, grid_color, (0, y), (VIRTUAL_WIDTH, y), 1)

def main():
    """Main entry point for the standalone multiplayer client."""
    print("================================")
    print("    MULTIPLAYER PACMAN DSA      ")
    print("================================")
    ip = input("Enter server IP (press Enter for localhost): ").strip()
    if not ip:
        ip = "127.0.0.1"
        
    role_choice = input("Enter role (1 for Pacman, 2 for Ghost): ").strip()
    requested_role = "ghost" if role_choice == "2" else "pacman"
    
    print("Connecting...")
    n = Network(host=ip, port=5555)
    player_id = n.p_id
    if player_id is None:
        print("Failed to connect to server (server may be full).")
        input("Press Enter to exit...")
        return
        
    role_info = n.send_init(requested_role)
    
    if role_info is None:
        print("Failed to receive role assignment.")
        input("Press Enter to exit...")
        return
    
    # Handle error (room full after connection)
    if role_info.get("type") == "error":
        print(f"Error: {role_info['message']}")
        input("Press Enter to exit...")
        return
    
    assigned_role = role_info.get("role", requested_role)
    if assigned_role != requested_role:
        print(f"⚠ Pac-Man slot is already taken! You have been assigned as GHOST.")
    
    print(f"Connected as Player {player_id} playing as {assigned_role.upper()}")
    print(f"Room: {role_info.get('player_count', '?')}/{role_info.get('max_players', '?')} players")
    
    if assigned_role == "pacman":
        print("★ You are the PAC-MAN! Press SPACE in the lobby to start the game.")
    else:
        print("👻 You are a GHOST! Waiting for Pac-Man to start the game...")
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Multiplayer Pacman Client")
    
    # Load fonts
    try:
        font_arcade = pygame.font.Font("../PressStart2P-Regular.ttf", 18)
        font_small = pygame.font.Font("../PressStart2P-Regular.ttf", 12)
        font_large = pygame.font.Font("../PressStart2P-Regular.ttf", 28)
        font_medium = pygame.font.Font("../PressStart2P-Regular.ttf", 16)
    except:
        font_arcade = pygame.font.SysFont('Courier', 18, bold=True)
        font_small = pygame.font.SysFont('Courier', 12, bold=True)
        font_large = pygame.font.SysFont('Courier', 28, bold=True)
        font_medium = pygame.font.SysFont('Courier', 16, bold=True)
        
    clock = pygame.time.Clock()
    wall_surface = None
    action = {"dr": 0, "dc": 0}
    
    running = True
    in_lobby = True
    game_started_local = False
    
    popups = []
    particles = []
    
    def spawn_particles(px, py, color, amount):
        import random
        for _ in range(amount):
            sx = random.uniform(-3, 3)
            sy = random.uniform(-3, 3)
            life = random.randint(15, 30)
            particles.append({"x": px, "y": py, "color": color, "sx": sx, "sy": sy, "life": life, "max_life": life})
    
    while running:
        virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and in_lobby and assigned_role == "pacman":
                    # Pac-Man starts the game
                    state = n.send({"type": "start_game"})
                    if state and state.get("game_started"):
                        in_lobby = False
                        game_started_local = True
                elif not in_lobby:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        action = {"dr": -1, "dc": 0}
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        action = {"dr": 1, "dc": 0}
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        action = {"dr": 0, "dc": -1}
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        action = {"dr": 0, "dc": 1}

        if in_lobby:
            # ── LOBBY SCREEN ──
            # Poll server for game state (to detect if game started)
            state = n.send({"dr": 0, "dc": 0})
            if not state:
                print("Disconnected from server.")
                break
            
            if state.get("type") == "game_state" and state.get("game_started"):
                in_lobby = False
                game_started_local = True
                continue
            
            # Draw lobby UI
            draw_synthwave_bg(virtual_surface)
            
            # Title
            title = font_large.render("LOBBY", True, YELLOW)
            virtual_surface.blit(title, (VIRTUAL_WIDTH // 2 - title.get_width() // 2, 60))
            
            # Room info
            p_count = state.get("player_count", 0) if isinstance(state, dict) else 0
            max_p = state.get("max_players", MAX_PLAYERS) if isinstance(state, dict) else MAX_PLAYERS
            
            room_text = font_medium.render(f"Players: {p_count}/{max_p}", True, WHITE)
            virtual_surface.blit(room_text, (VIRTUAL_WIDTH // 2 - room_text.get_width() // 2, 120))
            
            # Player's role
            if assigned_role == "pacman":
                role_color = YELLOW
                role_label = "YOU ARE PAC-MAN"
            else:
                role_color = (255, 100, 100)
                role_label = "YOU ARE A GHOST"
            
            role_text = font_arcade.render(role_label, True, role_color)
            virtual_surface.blit(role_text, (VIRTUAL_WIDTH // 2 - role_text.get_width() // 2, 180))
            
            # Draw player slots
            slot_y = 250
            if isinstance(state, dict) and "pacmans" in state:
                pac_players = state.get("pacmans", [])
                ghost_players = [g for g in state.get("ghosts", []) if g.get("is_player")]
                all_players = pac_players + ghost_players
            else:
                all_players = []

            for i in range(max_p):
                slot_x = VIRTUAL_WIDTH // 2 - 150
                slot_w = 300
                slot_h = 50
                
                # Slot background
                if i < len(all_players):
                    p_data = all_players[i]
                    # Filled slot
                    pygame.draw.rect(virtual_surface, (30, 60, 30), (slot_x, slot_y, slot_w, slot_h))
                    pygame.draw.rect(virtual_surface, (0, 200, 80), (slot_x, slot_y, slot_w, slot_h), 2)
                    
                    if "score" in p_data: # is pacman
                        slot_label = font_small.render(f"PLAYER {p_data['pid']}  -  PAC-MAN", True, YELLOW)
                    else:
                        color = p_data["color"]
                        if color == (255, 184, 82): c_name = "ORANGE"
                        elif color == (0, 255, 255): c_name = "CYAN"
                        elif color == (180, 80, 255): c_name = "PURPLE"
                        elif color == (255, 120, 120): c_name = "L-RED"
                        elif color == (255, 0, 0): c_name = "RED"
                        elif color == (255, 184, 255): c_name = "PINK"
                        else: c_name = "GHOST"
                        slot_label = font_small.render(f"PLAYER {p_data['pid']}  -  {c_name} GHOST", True, color)
                    virtual_surface.blit(slot_label, (slot_x + 20, slot_y + 18))
                else:
                    # Empty slot
                    pygame.draw.rect(virtual_surface, (20, 20, 40), (slot_x, slot_y, slot_w, slot_h))
                    pygame.draw.rect(virtual_surface, (60, 60, 80), (slot_x, slot_y, slot_w, slot_h), 2)
                    
                    empty_label = font_small.render(f"SLOT {i+1}  -  EMPTY", True, (60, 60, 80))
                    virtual_surface.blit(empty_label, (slot_x + 20, slot_y + 18))
                
                slot_y += 60
            
            # Instructions
            if assigned_role == "pacman":
                # Pulsing "Press SPACE" text
                pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
                alpha = int(128 + 127 * pulse)
                start_text = font_arcade.render("Press SPACE to START", True, (0, alpha, 0))
                virtual_surface.blit(start_text, (VIRTUAL_WIDTH // 2 - start_text.get_width() // 2, slot_y + 30))
            else:
                wait_text = font_small.render("Waiting for Pac-Man to start...", True, GRAY)
                virtual_surface.blit(wait_text, (VIRTUAL_WIDTH // 2 - wait_text.get_width() // 2, slot_y + 30))
            
            esc_text = font_small.render("Press ESC to leave", True, (80, 80, 80))
            virtual_surface.blit(esc_text, (VIRTUAL_WIDTH // 2 - esc_text.get_width() // 2, VIRTUAL_HEIGHT - 40))
            
        else:
            # ── GAME SCREEN ──
            # Send action & receive state
            state = n.send(action)
            if not state:
                print("Disconnected from server.")
                break
                
            # Parse state
            grid = state.get("grid", [])
            if wall_surface is None and grid:
                wall_surface = create_wall_surface(grid)
                
            # Process effects
            for eff in state.get("effects", []):
                r, c = eff["r"], eff["c"]
                px = c * CELL_SIZE
                py = r * CELL_SIZE + UI_OFFSET_Y
                
                if eff["type"] == "energizer":
                    popups.append({"text": "+50", "x": px, "y": py, "timer": 60, "color": (255, 255, 50)})
                    spawn_particles(px + CELL_SIZE//2, py + CELL_SIZE//2, (255, 255, 50), 20)
                elif eff["type"] == "dot":
                    popups.append({"text": "+10", "x": px, "y": py, "timer": 30, "color": (255, 255, 255)})
                    spawn_particles(px + CELL_SIZE//2, py + CELL_SIZE//2, (255, 255, 255), 5)
                elif eff["type"] == "ghost":
                    popups.append({"text": "+200", "x": px, "y": py, "timer": 60, "color": (0, 255, 255)})
                    spawn_particles(px + CELL_SIZE//2, py + CELL_SIZE//2, (0, 255, 255), 30)
                    
            # Draw background and map
            draw_synthwave_bg(virtual_surface)
            if wall_surface:
                virtual_surface.blit(wall_surface, (0, 0))
            draw_items(virtual_surface, grid)
            
            # Sync Pacmans
            scores = []
            for p_data in state.get("pacmans", []):
                p = Pacman(p_data["r"], p_data["c"])
                p.dr = p_data["dr"]
                p.dc = p_data["dc"]
                if p.dr != 0 or p.dc != 0:
                    p.facing_dr = p.dr
                    p.facing_dc = p.dc
                p.color = p_data["color"]
                p.score = p_data["score"]
                p.lives = p_data["lives"]
                p.draw(virtual_surface)
                scores.append((p.score, p.color, p.lives))
                
            # Sync Ghosts
            for g_data in state.get("ghosts", []):
                g = Ghost(g_data["r"], g_data["c"], g_data["color"])
                g.frightened_timer = 1 if g_data["frightened"] else 0
                g.is_dead = g_data["dead"]
                g.dr = g_data["dr"]
                g.dc = g_data["dc"]
                g.draw(virtual_surface)
                
            # UI rendering
            if len(scores) > 0:
                # Pac-Man score (top left)
                t_label = font_small.render("PAC-MAN", True, YELLOW)
                virtual_surface.blit(t_label, (20, 3))
                t_score = font_arcade.render(str(scores[0][0]), True, WHITE)
                virtual_surface.blit(t_score, (20, 20))
                
                # Lives display
                lives = scores[0][2]
                for i in range(lives):
                    lx = 30 + i * 30
                    ly = VIRTUAL_HEIGHT - 25
                    pygame.gfxdraw.filled_circle(virtual_surface, lx, ly, 10, YELLOW)
                    pygame.draw.polygon(virtual_surface, (10, 0, 20), [(lx, ly), (lx+12, ly-6), (lx+12, ly+6)])
                    
            # Update and Draw Particles
            for p in particles[:]:
                p["x"] += p["sx"]
                p["y"] += p["sy"]
                p["life"] -= 1
                if p["life"] <= 0:
                    particles.remove(p)
                else:
                    size = max(1, int(3 * (p["life"] / p["max_life"])))
                    pygame.draw.circle(virtual_surface, p["color"], (int(p["x"]), int(p["y"])), size)

            # Update and Draw Popups
            for p in popups[:]:
                p["timer"] -= 1
                p["y"] -= 0.5
                if p["timer"] <= 0:
                    popups.remove(p)
                else:
                    text_surf = font_small.render(p["text"], True, p["color"])
                    virtual_surface.blit(text_surf, (int(p["x"]), int(p["y"])))
                
            # Check Game Over
            if state.get("game_over"):
                end_text = font_large.render("GAME OVER", True, (255, 50, 50))
                virtual_surface.blit(end_text, (VIRTUAL_WIDTH // 2 - end_text.get_width() // 2, VIRTUAL_HEIGHT // 2))
                
            # Player count indicator (top right)
            pc = state.get("player_count", 0)
            pc_text = font_small.render(f"{pc} ONLINE", True, (0, 200, 80))
            virtual_surface.blit(pc_text, (VIRTUAL_WIDTH - pc_text.get_width() - 10, 5))
            
            # Your role indicator
            if assigned_role == "pacman":
                role_indicator = font_small.render("YOU: PAC-MAN", True, YELLOW)
            else:
                role_indicator = font_small.render("YOU: GHOST", True, (255, 100, 100))
            virtual_surface.blit(role_indicator, (VIRTUAL_WIDTH - role_indicator.get_width() - 10, 22))
                
        # Scale to fit actual screen
        screen.fill(BLACK)
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
