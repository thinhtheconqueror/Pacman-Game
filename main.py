"""
main.py

This is the main entry point for the Pacman DSA project.
It handles the game loop, menu system, and orchestrates the interaction
between the map data, entities, and pathfinding algorithms.
"""

import pygame
import pygame.gfxdraw
import sys
import math
import random
from settings import *
from map_data import load_map_matrix
from entities import Pacman, Ghost

def create_wall_surface(grid):
    """
    Creates a static glowing surface for the map walls.
    """
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
                    dot_c = (255, 50, 150) # Hot pink dots
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(dot_r + 4), (*dot_c, 50))
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(dot_r), dot_c)
                elif val == '2':
                    eng_r = 6 + pulse * 3
                    eng_c = (255, 255, 50) # Neon yellow energizers
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(eng_r + 6), (*eng_c, 80))
                    pygame.gfxdraw.filled_circle(surface, cx, cy, int(eng_r), eng_c)

def initial_spawns(grid, is_hard_mode, ghost_count_limit):
    """
    Initializes Pacman and Ghost objects from map markers ('P' and 'E').
    
    Args:
        grid (list[list[str]]): The map grid (will be modified to remove markers).
        is_hard_mode (bool): AI difficulty setting.
        ghost_count_limit (int): Maximum number of ghosts to spawn.
        
    Returns:
        tuple: (Pacman, list[Ghost]) objects.
    """
    pacman = None
    ghosts = []
    
    # Track the color index or ghost types (e.g. Blinky = Red)
    ghost_colors = [RED, PINK, CYAN, ORANGE]
    ghost_types = ["Blinky", "Pinky", "Inky", "Clyde"]
    ghost_count = 0
    
    for r in range(ROWS):
        for c in range(COLS):
            val = grid[r][c]
            if val == 'P':
                pacman = Pacman(r, c)
                grid[r][c] = ' ' # Clear the spawn marker after creating
            elif val == 'E':
                if ghost_count < ghost_count_limit:
                    color = ghost_colors[ghost_count % len(ghost_colors)]
                    gtype = ghost_types[ghost_count % len(ghost_types)]
                    ghost = Ghost(r, c, color, is_hard_mode=is_hard_mode, ghost_type=gtype)
                    ghosts.append(ghost)
                    ghost_count += 1
                grid[r][c] = ' ' # Always clear spawn marker
                
    return pacman, ghosts

def main_menu(screen, font):
    """
    Displays the splash screen and difficulty selection menu.
    
    Blocks execution until a selection is made by the user.
    
    Args:
        screen (pygame.Surface): The game window surface.
        font (pygame.font.Font): Font used for text rendering.
        
    Returns:
        tuple: (bool is_hard_mode, int ghost_count) based on user input.
    """
    ghost_count = 4 # Default
    while True:
        screen.fill(BLACK)
        virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        virtual_surface.fill(BLACK)
        
        font_small = ASSETS.get('font', font)
        
        title = font.render("PACMAN DSA PROJECT", True, YELLOW)
        opt_ghost = font_small.render(f"Ghosts: {ghost_count} (UP/DOWN)", True, CYAN)
        opt1 = font_small.render("Press '1': Easy", True, WHITE)
        opt2 = font_small.render("Press '2': Hard", True, RED)
        
        virtual_surface.blit(title, (VIRTUAL_WIDTH//2 - title.get_width()//2, VIRTUAL_HEIGHT//4))
        virtual_surface.blit(opt_ghost, (VIRTUAL_WIDTH//2 - opt_ghost.get_width()//2, VIRTUAL_HEIGHT//2 - 20))
        virtual_surface.blit(opt1, (VIRTUAL_WIDTH//2 - opt1.get_width()//2, VIRTUAL_HEIGHT//2 + 30))
        virtual_surface.blit(opt2, (VIRTUAL_WIDTH//2 - opt2.get_width()//2, VIRTUAL_HEIGHT//2 + 70))
        
        # Scale and draw to actual screen
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ghost_count = min(4, ghost_count + 1)
                elif event.key == pygame.K_DOWN:
                    ghost_count = max(1, ghost_count - 1)
                elif event.key == pygame.K_1:
                    return False, ghost_count # Easy
                elif event.key == pygame.K_2:
                    return True, ghost_count  # Hard Mode

def randomize_energizers(grid, count=4, min_dist=10):
    """Randomly places energizers on the grid, ensuring they are spaced apart."""
    potential_spots = []
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == '2':
                grid[r][c] = '0'
            if grid[r][c] == '0':
                potential_spots.append((r, c))
                
    selected = []
    attempts = 0
    while len(selected) < count and attempts < 200:
        attempts += 1
        spot = random.choice(potential_spots)
        too_close = False
        for sr, sc in selected:
            if math.hypot(sr - spot[0], sc - spot[1]) < min_dist:
                too_close = True
                break
        if not too_close:
            selected.append(spot)
            potential_spots.remove(spot)
            
    # Fallback if too strict
    while len(selected) < count and potential_spots:
        spot = random.choice(potential_spots)
        selected.append(spot)
        potential_spots.remove(spot)
        
    for r, c in selected:
        grid[r][c] = '2'

def draw_synthwave_bg(surface):
    """Draws a moving 2026 outrun / synthwave grid background."""
    time_ms = pygame.time.get_ticks()
    # Deep purple background
    surface.fill((10, 0, 20, 255))
    
    # Moving grid
    offset = (time_ms * 0.05) % CELL_SIZE
    grid_color = (40, 10, 80, 255)
    
    for c in range(0, COLS + 1):
        x = c * CELL_SIZE
        pygame.draw.line(surface, grid_color, (x, 0), (x, VIRTUAL_HEIGHT), 1)
        
    for r in range(-1, ROWS + 1):
        y = r * CELL_SIZE + offset
        pygame.draw.line(surface, grid_color, (0, y), (VIRTUAL_WIDTH, y), 1)

def game_loop(screen, font, is_hard_mode, ghost_count, clock):
    """
    Manages the core game state, input handling, and rendering.
    
    Runs a while loop that processes events, updates entity logic,
    and draws the game board 60 times per second.
    
    Args:
        screen (pygame.Surface): The game window.
        font (pygame.font.Font): Font for UI text.
        is_hard_mode (bool): Flag for advanced AI pathfinding.
        ghost_count (int): Number of ghosts to include.
        clock (pygame.time.Clock): Pygame ticker for FPS control.
    """
    # Load 2D Array State
    grid_matrix = load_map_matrix()
    randomize_energizers(grid_matrix, count=4, min_dist=10)
    
    wall_surface = create_wall_surface(grid_matrix)
    
    pacman, ghosts = initial_spawns(grid_matrix, is_hard_mode, ghost_count)
    
    if not pacman:
        print("ERROR: Pacman ('P') not found in map_data layout!")
        sys.exit()
    
    # Game Loop state variables
    running = True
    game_over = False
    hit_stop_frames = 0
    dots_total = sum(row.count('0') + row.count('2') for row in grid_matrix)
    immunity = False
    popups = []
    particles = []
    font_small = ASSETS.get('font', pygame.font.SysFont('Arial', 16, bold=True))
    
    def spawn_particles(px, py, color, amount):
        for _ in range(amount):
            sx = random.uniform(-3, 3)
            sy = random.uniform(-3, 3)
            life = random.randint(15, 30)
            particles.append({"x": px, "y": py, "color": color, "sx": sx, "sy": sy, "life": life, "max_life": life})
    
    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        sounds = {
            'eat': pygame.mixer.Sound('eating.mp3'),
            'energizer': pygame.mixer.Sound('eat-pill.mp3'),
            'ghost': pygame.mixer.Sound('eat-ghost.mp3'),
            'siren': pygame.mixer.Sound('siren.mp3')
        }
        eat_channel = pygame.mixer.Channel(0)
        siren_channel = pygame.mixer.Channel(1)
        ghost_channel = pygame.mixer.Channel(2)
        
        siren_channel.play(sounds['siren'], loops=-1)
        siren_playing = True
    except Exception as e:
        print("Could not load sounds:", e)
        sounds = {}
        eat_channel = siren_channel = ghost_channel = None
        siren_playing = False
        
    while running:
        virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        # 1. Handle Events (Input Queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_ALT:
                    if event.key == pygame.K_i:
                        immunity = not immunity
                    elif event.key == pygame.K_e:
                        for r in range(ROWS):
                            for c in range(COLS):
                                if grid_matrix[r][c] in ['0', '2']:
                                    grid_matrix[r][c] = ' '
                        dots_total = 0
                        game_over = True
                        if siren_playing and siren_channel:
                            siren_channel.stop()
                            siren_playing = False
                    elif event.key == pygame.K_x:
                        for ghost in ghosts:
                            ghost.die()
                elif game_over:
                    if event.key == pygame.K_r:
                        if siren_channel: siren_channel.stop()
                        return # Break out to restart back to menu
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        if siren_channel: siren_channel.stop()
                        return
                else:
                    if event.key == pygame.K_ESCAPE:
                        if siren_channel: siren_channel.stop()
                        return # Back to menu
                    elif event.key == pygame.K_r:
                        if siren_channel: siren_channel.stop()
                        return # Restart mid-game
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        pacman.set_direction(-1, 0)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        pacman.set_direction(1, 0)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        pacman.set_direction(0, -1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        pacman.set_direction(0, 1)

        if not game_over:
            is_frozen = False
            if hit_stop_frames > 0:
                hit_stop_frames -= 1
                is_frozen = True
                
            if not is_frozen:
                # 2. Update Grid Entities (Logic / Simulation)
                pacman.update(grid_matrix)
                
                dot_eaten = pacman.check_eat_dot(grid_matrix)
                if dot_eaten:
                    dots_total -= 1
                    px, py = pacman.c * CELL_SIZE, pacman.r * CELL_SIZE + UI_OFFSET_Y
                    if dot_eaten == 'ENERGIZER':
                        pacman.power_timer = FPS * 4
                        if 'energizer' in sounds and eat_channel: eat_channel.play(sounds['energizer'])
                        for ghost in ghosts:
                            ghost.frighten()
                        popups.append({"text": "+50", "x": px, "y": py, "timer": FPS, "color": ENERGIZER_COLOR})
                        spawn_particles(px + CELL_SIZE//2, py + CELL_SIZE//2, ENERGIZER_COLOR, 20)
                    else:
                        if 'eat' in sounds and eat_channel and not eat_channel.get_busy():
                            eat_channel.play(sounds['eat'])
                        popups.append({"text": "+10", "x": px, "y": py, "timer": FPS // 2, "color": WHITE})
                        spawn_particles(px + CELL_SIZE//2, py + CELL_SIZE//2, WHITE, 5)
                    if dots_total <= 0:
                        game_over = True # Win State
                        if siren_playing and siren_channel:
                            siren_channel.stop()
                            siren_playing = False
                        
                # 3. Update Ghosts (AI Pathfinding logic)
                for ghost in ghosts:
                    ghost.update(pacman, grid_matrix, ghosts)
                    
                    # Check Death condition
                    if ghost.r == pacman.r and ghost.c == pacman.c and not ghost.is_dead:
                        if ghost.frightened_timer > 0:
                            if 'ghost' in sounds and ghost_channel: ghost_channel.play(sounds['ghost'])
                            gx, gy = ghost.c * CELL_SIZE, ghost.r * CELL_SIZE + UI_OFFSET_Y
                            ghost.die()
                            hit_stop_frames = 30 # Freeze for half a second
                            pacman.score += 200
                            popups.append({"text": "+200", "x": gx, "y": gy, "timer": FPS, "color": CYAN})
                            spawn_particles(gx + CELL_SIZE//2, gy + CELL_SIZE//2, CYAN, 30)
                        elif not immunity:
                            pacman.lives -= 1
                            if pacman.lives <= 0:
                                game_over = True # Loss state
                                if siren_playing and siren_channel:
                                    siren_channel.stop()
                                    siren_playing = False
                            else:
                                pacman.r, pacman.c = pacman.start_r, pacman.start_c
                                for g in ghosts:
                                    g.r, g.c = g.start_r, g.start_c
                                    g.is_dead = False
                                    g.frightened_timer = 0
                                    g.respawn_timer = 0
        
        # 4. Draw/Render Output
        draw_synthwave_bg(virtual_surface)
        
        virtual_surface.blit(wall_surface, (0, 0))
        draw_items(virtual_surface, grid_matrix)
        
        if not game_over:
            pacman.draw(virtual_surface)
            for ghost in ghosts:
                ghost.draw(virtual_surface)
                
        # Draw Particles
        for p in particles[:]:
            p["x"] += p["sx"]
            p["y"] += p["sy"]
            p["life"] -= 1
            if p["life"] <= 0:
                particles.remove(p)
            else:
                size = max(1, int(3 * (p["life"] / p["max_life"])))
                pygame.draw.circle(virtual_surface, p["color"], (int(p["x"]), int(p["y"])), size)

        # Draw Popups
        for p in popups[:]:
            p["timer"] -= 1
            p["y"] -= 0.5 # Float up
            if p["timer"] <= 0:
                popups.remove(p)
            else:
                text_surf = font_small.render(p["text"], True, p["color"])
                virtual_surface.blit(text_surf, (p["x"], p["y"]))
        
        # Draw Classic Arcade UI
        font_arcade = ASSETS.get('font', pygame.font.SysFont('Courier', 18, bold=True))
        
        # TOP UI
        t_1up = font_arcade.render("1UP", True, WHITE)
        t_high = font_arcade.render("HIGH SCORE", True, WHITE)
        t_2up = font_arcade.render("2UP", True, WHITE)
        
        virtual_surface.blit(t_1up, (70, 5))
        virtual_surface.blit(t_high, (VIRTUAL_WIDTH//2 - t_high.get_width()//2, 5))
        virtual_surface.blit(t_2up, (VIRTUAL_WIDTH - 100, 5))
        
        t_score1 = font_arcade.render(str(pacman.score), True, WHITE)
        t_scoreH = font_arcade.render("10000", True, WHITE)
        t_score2 = font_arcade.render("0", True, WHITE)
        
        virtual_surface.blit(t_score1, (70 + t_1up.get_width()//2 - t_score1.get_width()//2, 25))
        virtual_surface.blit(t_scoreH, (VIRTUAL_WIDTH//2 - t_scoreH.get_width()//2, 25))
        virtual_surface.blit(t_score2, (VIRTUAL_WIDTH - 100 + t_2up.get_width()//2 - t_score2.get_width()//2, 25))
        
        # BOTTOM UI
        # Lives
        for i in range(pacman.lives):
            px = 30 + i * 30
            py = VIRTUAL_HEIGHT - 25
            pygame.gfxdraw.filled_circle(virtual_surface, px, py, 10, YELLOW)
            pygame.draw.polygon(virtual_surface, (10, 0, 20), [(px, py), (px+12, py-6), (px+12, py+6)])
            
        # Cherries
        cx, cy = VIRTUAL_WIDTH - 40, VIRTUAL_HEIGHT - 25
        pygame.gfxdraw.filled_circle(virtual_surface, cx - 6, cy + 4, 6, RED)
        pygame.gfxdraw.filled_circle(virtual_surface, cx + 6, cy + 4, 6, RED)
        pygame.draw.line(virtual_surface, (0, 255, 0), (cx - 6, cy - 2), (cx, cy - 10), 2)
        pygame.draw.line(virtual_surface, (0, 255, 0), (cx + 6, cy - 2), (cx, cy - 10), 2)
        
        # Game Over / Win UI
        if game_over:
            if dots_total <= 0:
                end_text = font.render("YOU WIN! All Dots Eaten!", True, YELLOW)
            else:
                end_text = font.render("GAME OVER - Eaten by Ghost!", True, RED)
            virtual_surface.blit(end_text, (VIRTUAL_WIDTH//2 - end_text.get_width()//2, VIRTUAL_HEIGHT//2))
            
            # Draw restart prompt
            restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
            virtual_surface.blit(restart_text, (VIRTUAL_WIDTH//2 - restart_text.get_width()//2, VIRTUAL_HEIGHT//2 + 40))
        
        # Scale to fit actual screen
        screen.fill(BLACK)
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        
        pygame.display.flip()
        
        # Note: 60 FPS, but ghosts move every 15 frames for balancing
        clock.tick(FPS)

def load_arcade_assets():
    try:
        sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = sheet.get_at((0,0))
        sheet.set_colorkey(transcolor)
        
        def get_sprite(x, y, w=32, h=32):
            rect = pygame.Rect(x * 16, y * 16, w, h)
            sub = sheet.subsurface(rect)
            return pygame.transform.smoothscale(sub, (CELL_SIZE + 6, CELL_SIZE + 6))
            
        ASSETS['pacman_L'] = get_sprite(8, 0)
        ASSETS['pacman_R'] = get_sprite(10, 0)
        ASSETS['pacman_U'] = get_sprite(10, 2)
        ASSETS['pacman_D'] = get_sprite(8, 2)
        
        ASSETS['ghost_red'] = get_sprite(0, 4)
        ASSETS['ghost_pink'] = get_sprite(2, 4)
        ASSETS['ghost_cyan'] = get_sprite(4, 4)
        ASSETS['ghost_orange'] = get_sprite(6, 4)
        
        ASSETS['ghost_frightened'] = get_sprite(10, 4)
        
        ASSETS['eyes_U'] = get_sprite(8, 4)
        ASSETS['eyes_D'] = get_sprite(8, 6)
        ASSETS['eyes_L'] = get_sprite(8, 8)
        ASSETS['eyes_R'] = get_sprite(8, 10)
        
        ASSETS['font'] = pygame.font.Font("PressStart2P-Regular.ttf", 16)
        ASSETS['font_large'] = pygame.font.Font("PressStart2P-Regular.ttf", 24)
    except Exception as e:
        print("Failed to load arcade assets:", e)

def main():
    """
    Initializes the Pygame environment and enters the main menu cycle.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("DSA Pacman Project - BFS AI")
    
    load_arcade_assets()
    
    clock = pygame.time.Clock()
    font = ASSETS.get('font_large', pygame.font.SysFont('Arial', 24, bold=True))
    
    while True:
        # Loop endlessly. main_menu blocks until user selects a mode
        is_hard_mode, ghost_count = main_menu(screen, font)
        game_loop(screen, font, is_hard_mode, ghost_count, clock)

if __name__ == "__main__":
    main()
