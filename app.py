"""
app.py

This module serves as the primary launcher for the Pacman application,
providing an interface to choose between offline and multiplayer modes.
It handles server process management, network connections, and UI screens.
"""

import pygame
import sys
import threading
import subprocess
import os
import socket

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

from settings import *

def get_local_ip():
    """Get this machine's LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def kill_server_on_port(port=5555):
    """Kill any existing process listening on the given port (Windows)."""
    try:
        result = subprocess.run(
            ['netstat', '-ano'], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = int(parts[-1])
                if pid > 0:
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                   capture_output=True)
                    print(f"Killed old server process (PID {pid})")
    except Exception as e:
        pass  # Silently ignore if can't find/kill

# Import the offline main menu and loop
from main import game_loop as offline_game_loop, main_menu as offline_main_menu, load_arcade_assets

def run_offline(screen, font, clock):
    """
    Runs the game in offline mode.
    
    Args:
        screen (pygame.Surface): The main display surface.
        font (pygame.font.Font): The font used for text rendering.
        clock (pygame.time.Clock): The pygame clock for frame rate control.
    """
    is_hard_mode, ghost_count = offline_main_menu(screen, font)
    offline_game_loop(screen, font, is_hard_mode, ghost_count, clock)

def draw_text_center(surface, text, font, color, y):
    """
    Draws text centered horizontally on the given surface at a specific y-coordinate.
    
    Args:
        surface (pygame.Surface): The surface to draw on.
        text (str): The text to render.
        font (pygame.font.Font): The font to use.
        color (tuple): RGB color of the text.
        y (int): The y-coordinate to draw the text at.
    """
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (VIRTUAL_WIDTH//2 - text_surf.get_width()//2, y))
    
def input_screen(screen, virtual_surface, font, prompt, default_val=""):
    """
    Displays an input screen for the user to type text.
    
    Args:
        screen (pygame.Surface): The main display surface.
        virtual_surface (pygame.Surface): The virtual resolution surface.
        font (pygame.font.Font): The font to use for rendering text.
        prompt (str): The prompt text to display.
        default_val (str): Default value in the input box.
        
    Returns:
        str: The string input entered by the user.
    """
    clock = pygame.time.Clock()
    user_text = default_val
    input_active = True
    
    while input_active:
        virtual_surface.fill(BLACK)
        
        draw_text_center(virtual_surface, prompt, font, YELLOW, VIRTUAL_HEIGHT // 3)
        
        # Draw input box
        box_w = 400
        box_h = 50
        box_x = VIRTUAL_WIDTH//2 - box_w//2
        box_y = VIRTUAL_HEIGHT // 2 - box_h//2
        pygame.draw.rect(virtual_surface, CYAN, (box_x, box_y, box_w, box_h), 3)
        
        text_surf = font.render(user_text, True, WHITE)
        virtual_surface.blit(text_surf, (box_x + 10, box_y + 15))
        
        draw_text_center(virtual_surface, "Press ENTER to confirm", font, GRAY, VIRTUAL_HEIGHT // 2 + 60)
        
        # Scale to fit actual screen
        screen.fill(BLACK)
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
                if event.key == pygame.K_RETURN:
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 20:
                        user_text += event.unicode
        clock.tick(60)

def role_selection_screen(screen, virtual_surface, font):
    """
    Displays a screen for the user to select their role (Pacman or Ghost).
    
    Args:
        screen (pygame.Surface): The main display surface.
        virtual_surface (pygame.Surface): The virtual resolution surface.
        font (pygame.font.Font): The font used for text.
        
    Returns:
        str: The selected role, either 'pacman' or 'ghost'.
    """
    clock = pygame.time.Clock()
    
    while True:
        virtual_surface.fill(BLACK)
        
        draw_text_center(virtual_surface, "SELECT ROLE", font, YELLOW, VIRTUAL_HEIGHT // 3)
        
        draw_text_center(virtual_surface, "Press 1: PAC-MAN", font, YELLOW, VIRTUAL_HEIGHT // 2 - 20)
        draw_text_center(virtual_surface, "Press 2: GHOST", font, RED, VIRTUAL_HEIGHT // 2 + 30)
        
        # Scale
        screen.fill(BLACK)
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
                if event.key == pygame.K_1:
                    return "pacman"
                elif event.key == pygame.K_2:
                    return "ghost"
        clock.tick(60)

def show_message_screen(screen, virtual_surface, font, message, color, duration=120):
    """Show a temporary message screen for `duration` frames."""
    import math
    clock = pygame.time.Clock()
    for i in range(duration):
        virtual_surface.fill(BLACK)
        draw_text_center(virtual_surface, message, font, color, VIRTUAL_HEIGHT // 2)
        screen.fill(BLACK)
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

def run_multiplayer_client(screen, virtual_surface, font, ip, role, server_ip=None):
    """
    Runs the multiplayer client, connecting to a server and rendering game state.
    
    Args:
        screen (pygame.Surface): The main display surface.
        virtual_surface (pygame.Surface): The virtual resolution surface.
        font (pygame.font.Font): The font for text rendering.
        ip (str): The IP address of the server to connect to.
        role (str): The initial role selected by the user.
        server_ip (str, optional): The server IP if hosting locally.
    """
    import math
    # Dynamically import the multiplayer logic so it doesn't conflict with main.py
    sys.path.insert(0, os.path.join(current_dir, "Multiplayer_Python"))
    import network
    import client as mp_client
    import importlib
    importlib.reload(network)
    importlib.reload(mp_client)
    
    n = network.Network(host=ip, port=5555)
    if n.p_id is None:
        show_message_screen(screen, virtual_surface, font, "FAILED TO CONNECT (FULL?)", RED)
        sys.path.pop(0)
        return
        
    role_info = n.send_init(role)
    
    if role_info is None or role_info.get("type") == "error":
        msg = role_info.get("message", "CONNECTION ERROR") if role_info else "CONNECTION ERROR"
        show_message_screen(screen, virtual_surface, font, msg, RED)
        sys.path.pop(0)
        return
    
    assigned_role = role_info.get("role", role)
    was_reassigned = (assigned_role != role)
    
    if was_reassigned:
        show_message_screen(screen, virtual_surface, font, "PAC-MAN TAKEN! YOU ARE GHOST", (255, 150, 50), 90)
    
    font_arcade = pygame.font.Font("PressStart2P-Regular.ttf", 18)
    font_small = pygame.font.Font("PressStart2P-Regular.ttf", 11)
    font_lobby = pygame.font.Font("PressStart2P-Regular.ttf", 22)
    clock = pygame.time.Clock()
    wall_surface = None
    action = {"dr": 0, "dc": 0}
    in_lobby = True
    
    popups = []
    particles = []
    
    def spawn_particles(px, py, color, amount):
        import random
        for _ in range(amount):
            sx = random.uniform(-3, 3)
            sy = random.uniform(-3, 3)
            life = random.randint(15, 30)
            particles.append({"x": px, "y": py, "color": color, "sx": sx, "sy": sy, "life": life, "max_life": life})
    
    # Load sounds
    try:
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        sounds = {
            'eat': pygame.mixer.Sound('eating.mp3'),
            'energizer': pygame.mixer.Sound('eat-pill.mp3'),
            'ghost': pygame.mixer.Sound('eat-ghost.mp3'),
            'siren': pygame.mixer.Sound('siren.mp3'),
        }
        eat_channel = pygame.mixer.Channel(0)
        siren_channel = pygame.mixer.Channel(1)
        ghost_channel = pygame.mixer.Channel(2)
        siren_started = False
    except Exception as e:
        print("Could not load sounds:", e)
        sounds = {}
        eat_channel = siren_channel = ghost_channel = None
        siren_started = False
    
    role_c = YELLOW if assigned_role == "pacman" else (255, 100, 100)
    
    running = True
    while running:
        virtual_surface.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and in_lobby and assigned_role == "pacman":
                    state = n.send({"type": "start_game"})
                    if state and state.get("game_started"):
                        in_lobby = False
                    continue
                elif not in_lobby:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        action = {"dr": -1, "dc": 0}
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        action = {"dr": 1, "dc": 0}
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        action = {"dr": 0, "dc": -1}
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        action = {"dr": 0, "dc": 1}

        if in_lobby:
            state = n.send({"dr": 0, "dc": 0})
            if not state:
                running = False
                break
            if isinstance(state, dict) and state.get("game_started"):
                in_lobby = False
                continue
            
            # Draw lobby
            mp_client.draw_synthwave_bg(virtual_surface)
            title = font_lobby.render("LOBBY", True, YELLOW)
            virtual_surface.blit(title, (VIRTUAL_WIDTH//2 - title.get_width()//2, 60))
            
            pc = state.get("player_count", 0) if isinstance(state, dict) else 0
            max_p = state.get("max_players", 5) if isinstance(state, dict) else 5
            room_t = font_small.render(f"Players: {pc}/{max_p}", True, WHITE)
            virtual_surface.blit(room_t, (VIRTUAL_WIDTH//2 - room_t.get_width()//2, 100))
            
            # Show server IP if hosting
            if server_ip:
                ip_t = font_small.render(f"Server IP: {server_ip}", True, (0, 255, 180))
                virtual_surface.blit(ip_t, (VIRTUAL_WIDTH//2 - ip_t.get_width()//2, 120))
                share_t = font_small.render("Share this IP!", True, GRAY)
                virtual_surface.blit(share_t, (VIRTUAL_WIDTH//2 - share_t.get_width()//2, 138))
            
            role_c = YELLOW if assigned_role == "pacman" else (255, 100, 100)
            role_l = "YOU: PAC-MAN" if assigned_role == "pacman" else "YOU: GHOST"
            role_t = font_arcade.render(role_l, True, role_c)
            virtual_surface.blit(role_t, (VIRTUAL_WIDTH//2 - role_t.get_width()//2, 160))
            
            slot_y = 210
            
            if isinstance(state, dict) and "pacmans" in state:
                pac_players = state.get("pacmans", [])
                ghost_players = [g for g in state.get("ghosts", []) if g.get("is_player")]
                all_players = pac_players + ghost_players
            else:
                all_players = []
                
            for i in range(max_p):
                sx = VIRTUAL_WIDTH//2 - 140
                sw, sh = 280, 45
                if i < len(all_players):
                    p_data = all_players[i]
                    pygame.draw.rect(virtual_surface, (30, 60, 30), (sx, slot_y, sw, sh))
                    pygame.draw.rect(virtual_surface, (0, 200, 80), (sx, slot_y, sw, sh), 2)
                    if "score" in p_data:
                        lbl = f"PLAYER {p_data['pid']} - PAC-MAN"
                        lbl_c = YELLOW
                    else:
                        color = p_data["color"]
                        if color == (255, 184, 82): c_name = "ORANGE"
                        elif color == (0, 255, 255): c_name = "CYAN"
                        elif color == (180, 80, 255): c_name = "PURPLE"
                        elif color == (255, 120, 120): c_name = "L-RED"
                        elif color == (255, 0, 0): c_name = "RED"
                        elif color == (255, 184, 255): c_name = "PINK"
                        else: c_name = "GHOST"
                        lbl = f"PLAYER {p_data['pid']} - {c_name} GHOST"
                        lbl_c = color
                else:
                    pygame.draw.rect(virtual_surface, (20, 20, 40), (sx, slot_y, sw, sh))
                    pygame.draw.rect(virtual_surface, (60, 60, 80), (sx, slot_y, sw, sh), 2)
                    lbl = f"SLOT {i+1} - EMPTY"
                    lbl_c = (60, 60, 80)
                lbl_t = font_small.render(lbl, True, lbl_c)
                virtual_surface.blit(lbl_t, (sx + 15, slot_y + 15))
                slot_y += 55
            
            if assigned_role == "pacman":
                pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
                a = int(128 + 127 * pulse)
                st = font_small.render("Press SPACE to START", True, (0, a, 0))
                virtual_surface.blit(st, (VIRTUAL_WIDTH//2 - st.get_width()//2, slot_y + 20))
            else:
                wt = font_small.render("Waiting for Pac-Man...", True, GRAY)
                virtual_surface.blit(wt, (VIRTUAL_WIDTH//2 - wt.get_width()//2, slot_y + 20))
        else:
            state = n.send(action)
            if not state:
                running = False
                break
            
            # Play sound events from server
            if not siren_started and siren_channel and 'siren' in sounds:
                siren_channel.play(sounds['siren'], loops=-1)
                siren_started = True
            for snd in state.get("sounds", []):
                if snd == 'eat' and eat_channel and 'eat' in sounds:
                    if not eat_channel.get_busy():
                        eat_channel.play(sounds['eat'])
                elif snd == 'energizer' and eat_channel and 'energizer' in sounds:
                    eat_channel.play(sounds['energizer'])
                elif snd == 'ghost' and ghost_channel and 'ghost' in sounds:
                    ghost_channel.play(sounds['ghost'])
            
            grid = state.get("grid", [])
            if wall_surface is None and grid:
                wall_surface = mp_client.create_wall_surface(grid)
                
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
                    
            mp_client.draw_synthwave_bg(virtual_surface)
            if wall_surface:
                virtual_surface.blit(wall_surface, (0, 0))
            mp_client.draw_items(virtual_surface, grid)
            
            scores = []
            for p_data in state.get("pacmans", []):
                p = mp_client.Pacman(p_data["r"], p_data["c"])
                p.dr, p.dc = p_data["dr"], p_data["dc"]
                if p.dr != 0 or p.dc != 0:
                    p.facing_dr, p.facing_dc = p.dr, p.dc
                p.color, p.score, p.lives = p_data["color"], p_data["score"], p_data["lives"]
                p.draw(virtual_surface)
                scores.append((p.score, p.color, p.lives))
            for g_data in state.get("ghosts", []):
                g = mp_client.Ghost(g_data["r"], g_data["c"], g_data["color"])
                g.frightened_timer = 1 if g_data["frightened"] else 0
                g.is_dead, g.dr, g.dc = g_data["dead"], g_data["dr"], g_data["dc"]
                g.draw(virtual_surface)
            
            if scores:
                t1 = font_small.render("PAC-MAN", True, YELLOW)
                virtual_surface.blit(t1, (20, 3))
                ts = font_arcade.render(str(scores[0][0]), True, WHITE)
                virtual_surface.blit(ts, (20, 18))
                
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
                font_large = pygame.font.Font("PressStart2P-Regular.ttf", 28)
                end_text = font_large.render("GAME OVER", True, (255, 50, 50))
                virtual_surface.blit(end_text, (VIRTUAL_WIDTH // 2 - end_text.get_width() // 2, VIRTUAL_HEIGHT // 2))

            pc = state.get("player_count", 0)
            pt = font_small.render(f"{pc} ONLINE", True, (0, 200, 80))
            virtual_surface.blit(pt, (VIRTUAL_WIDTH - pt.get_width() - 10, 5))
            ri = font_small.render("YOU: " + assigned_role.upper(), True, role_c)
            virtual_surface.blit(ri, (VIRTUAL_WIDTH - ri.get_width() - 10, 22))
            
        screen.fill(BLACK)
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        pygame.display.flip()
        clock.tick(FPS)
    
    # Stop sounds on exit
    if siren_channel:
        siren_channel.stop()
    try:
        pygame.mixer.stop()
    except:
        pass
        
    sys.path.pop(0)

def main():
    """
    Main application entry point. Initializes pygame, loads assets,
    and displays the main menu for selecting game modes.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Pacman Ultimate App")
    
    load_arcade_assets()
    
    font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    font_large = pygame.font.Font("PressStart2P-Regular.ttf", 24)
    clock = pygame.time.Clock()
    
    server_process = None
    server_ip = None
    font_ip = pygame.font.Font("PressStart2P-Regular.ttf", 13)
    
    while True:
        virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        virtual_surface.fill(BLACK)
        
        draw_text_center(virtual_surface, "PACMAN ULTIMATE", font_large, YELLOW, VIRTUAL_HEIGHT // 4)
        
        draw_text_center(virtual_surface, "Press 1: OFFLINE MODE", font, WHITE, VIRTUAL_HEIGHT // 2 - 40)
        draw_text_center(virtual_surface, "Press 2: HOST MULTIPLAYER SERVER", font, CYAN, VIRTUAL_HEIGHT // 2 + 10)
        draw_text_center(virtual_surface, "Press 3: JOIN MULTIPLAYER", font, (0, 255, 0), VIRTUAL_HEIGHT // 2 + 60)
        
        if server_process is not None and server_ip:
            draw_text_center(virtual_surface, "Server running!", font, RED, VIRTUAL_HEIGHT // 2 + 110)
            draw_text_center(virtual_surface, f"IP: {server_ip}  Port: 5555", font_ip, (0, 255, 180), VIRTUAL_HEIGHT // 2 + 140)
            draw_text_center(virtual_surface, "Share this IP with friends", font_ip, GRAY, VIRTUAL_HEIGHT // 2 + 165)
        
        draw_text_center(virtual_surface, "Press ESC to Quit", font, GRAY, VIRTUAL_HEIGHT - 50)
        
        # Scale and draw
        screen.fill(BLACK)
        scale_h = HEIGHT
        scale_w = int(VIRTUAL_WIDTH * (HEIGHT / VIRTUAL_HEIGHT))
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (scale_w, scale_h))
        screen.blit(scaled_surf, ((WIDTH - scale_w) // 2, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if server_process:
                    server_process.kill()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if server_process:
                        server_process.kill()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    run_offline(screen, font_large, clock)
                elif event.key == pygame.K_2:
                    # Kill any orphaned server from a previous run
                    kill_server_on_port(5555)
                    # Also kill our tracked process if still alive
                    if server_process is not None:
                        server_process.kill()
                        server_process.wait()
                        server_process = None
                    import time; time.sleep(0.3)  # Let port free up
                    server_script = os.path.join(current_dir, "Multiplayer_Python", "server.py")
                    server_process = subprocess.Popen([sys.executable, server_script])
                    server_ip = get_local_ip()
                    time.sleep(0.5)  # Let server bind the port
                    
                    role = role_selection_screen(screen, virtual_surface, font)
                    run_multiplayer_client(screen, virtual_surface, font, "127.0.0.1", role, server_ip=server_ip)
                elif event.key == pygame.K_3:
                    ip = input_screen(screen, virtual_surface, font, "Enter Server IP:")
                    if not ip:
                        ip = "127.0.0.1"
                    role = role_selection_screen(screen, virtual_surface, font)
                    run_multiplayer_client(screen, virtual_surface, font, ip, role)
                    
        clock.tick(60)

if __name__ == "__main__":
    main()
