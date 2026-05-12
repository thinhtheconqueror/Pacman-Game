"""
entities.py

This module defines the game entities (Pacman and Ghosts) using Object-Oriented Programming (OOP).
All entities inherit from a base Entity class and interact with the 2D grid matrix.
"""

import pygame
import pygame.gfxdraw
from settings import *
from map_data import GAME_MAP
from algorithms import bfs_shortest_path
import math

_glow_cache = {}
def get_glow_surface(color, radius):
    """
    Generates and caches a glowing visual effect surface for entities.
    
    Args:
        color (tuple): The RGB color for the glow.
        radius (int): The base radius of the entity to calculate glow extent.
        
    Returns:
        pygame.Surface: A transparent surface containing the glowing effect.
    """
    key = (color, radius)
    if key not in _glow_cache:
        surf = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
        center = (radius*2, radius*2)
        for i in range(radius*2, 0, -1):
            ratio = i / (radius*2)
            alpha = int(120 * (1 - ratio)**2)
            pygame.draw.circle(surf, (*color[:3], alpha), center, i)
        _glow_cache[key] = surf
    return _glow_cache[key]

class Entity:
    """
    Base class for all moving game objects.
    
    Attributes:
        r (int): Current row index in the grid.
        c (int): Current column index in the grid.
        color (tuple): RGB color for rendering.
    """
    def __init__(self, r, c, color):
        """
        Initializes an entity at the specified grid coordinates.
        
        Args:
            r (int): Row index.
            c (int): Column index.
            color (tuple): RGB color representation.
        """
        self.r = r  # Row index
        self.c = c  # Column index
        self.color = color
        
    def draw(self, surface):
        """Renders the entity onto the Pygame surface based on grid (row, col) coordinates."""
        # Calculate pixel coordinates (x, y) based on grid indexing (col, row)
        x = self.c * CELL_SIZE
        y = self.r * CELL_SIZE
        
        # Draw a simple circle at the center of the cell
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        
        # Glow
        glow = get_glow_surface(self.color, radius)
        surface.blit(glow, (center[0] - radius*2, center[1] - radius*2))
        
        pygame.draw.circle(surface, self.color, center, radius)

class Pacman(Entity):
    """
    The player-controlled character.
    
    Handles movement input, grid-based collision, and scoring.
    """
    def __init__(self, r, c):
        """
        Initializes Pacman with default state at the specified starting coordinates.
        
        Args:
            r (int): Starting row index.
            c (int): Starting column index.
        """
        super().__init__(r, c, YELLOW)
        self.start_r = r
        self.start_c = c
        self.lives = 3
        self.score = 0
        self.move_delay = 15 # 4 moves per second at 60 FPS
        self.move_timer = 0
        self.dr = 0
        self.dc = 0
        self.next_dr = 0
        self.next_dc = 0
        self.facing_dr = 0
        self.facing_dc = 1
        self.anim_tick = 0
        self.mouth_open = True
        self.power_timer = 0
        
    def set_direction(self, dr, dc):
        """
        Queues a movement direction to be applied at the next grid junction.
        
        Args:
            dr (int): Row delta (-1, 0, or 1).
            dc (int): Column delta (-1, 0, or 1).
        """
        self.next_dr = dr
        self.next_dc = dc
        
    def update(self, grid):
        """
        Logic for Pacman's movement and collision detection.
        
        Implements a frame-based delay to synchronize movement with the grid cells.
        Collision detection is O(1) by checking the target cell in the grid array.
        
        Args:
            grid (list[list[str]]): The current state of the game grid.
        """
        # Animate mouth every 5 frames
        self.anim_tick += 1
        if self.anim_tick % 5 == 0:
            self.mouth_open = not self.mouth_open

        if self.power_timer > 0:
            self.power_timer -= 1

        if self.dr == 0 and self.dc == 0 and self.next_dr == 0 and self.next_dc == 0:
            return # Not moving
            
        self.move_timer += 1
        current_delay = 9 if self.power_timer > 0 else self.move_delay
        if self.move_timer >= current_delay:
            self.move_timer = 0
            
            # Check queued direction first
            n_nr = self.r + self.next_dr
            n_nc = self.c + self.next_dc
            
            # Wrap around logic for tunnels
            if n_nc < 0:
                n_nc = COLS - 1
            elif n_nc >= COLS:
                n_nc = 0
                
            # Boundary check and Collision check for the QUEUED direction
            if 0 <= n_nr < ROWS and 0 <= n_nc < COLS and grid[n_nr][n_nc] not in ('1', 'D'):
                # Valid turn, apply it
                self.dr = self.next_dr
                self.dc = self.next_dc
                self.facing_dr = self.dr
                self.facing_dc = self.dc
                self.r = n_nr
                self.c = n_nc
            else:
                # Invalid turn, attempt to continue in CURRENT direction
                nr = self.r + self.dr
                nc = self.c + self.dc
                
                # Wrap around logic for current direction
                if nc < 0:
                    nc = COLS - 1
                elif nc >= COLS:
                    nc = 0
                    
                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] not in ('1', 'D'):
                    self.r = nr
                    self.c = nc
                else:
                    # Both Blocked, hit wall entirely
                    self.dr = 0
                    self.dc = 0
                    
    def check_eat_dot(self, grid_state):
        """
        Checks if Pacman is on a cell with a dot and consumes it.
        
        Args:
            grid_state (list[list[str]]): The mutable grid to be updated.
            
        Returns:
            bool: True if a dot was consumed, False otherwise.
        """
        if grid_state[self.r][self.c] == '0':
            grid_state[self.r][self.c] = ' ' # Dot consumed
            self.score += 10
            return 'DOT'
        elif grid_state[self.r][self.c] == '2':
            grid_state[self.r][self.c] = ' ' # Energizer consumed
            self.score += 50
            return 'ENERGIZER'
        return None

    def draw(self, surface):
        """Overrides base Entity draw for an animated Pac-Man."""
        x = self.c * CELL_SIZE
        y = self.r * CELL_SIZE + UI_OFFSET_Y
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        r = CELL_SIZE // 2 - 2
        
        # Glowing aura
        glow = get_glow_surface(self.color, r + 4)
        surface.blit(glow, (cx - (r+4)*2, cy - (r+4)*2))
        
        pac_surf = pygame.Surface((r*4, r*4))
        pac_surf.fill((1, 1, 1))
        pac_surf.set_colorkey((1, 1, 1))
        center = (r*2, r*2)
        
        # Base body
        pygame.gfxdraw.aacircle(pac_surf, center[0], center[1], r, self.color)
        pygame.gfxdraw.filled_circle(pac_surf, center[0], center[1], r, self.color)
        
        # Smooth Mouth open logic
        import math
        time_ms = pygame.time.get_ticks()
        mouth_angle = abs(math.sin(time_ms * 0.015)) * 45 # 0 to 45 degrees
        
        if mouth_angle > 2:
            f_dr, f_dc = self.facing_dr, self.facing_dc
            if f_dr == 0 and f_dc == 0:
                f_dc = 1 # Default right
                
            if f_dr == -1: base_angle = 270
            elif f_dr == 1: base_angle = 90
            elif f_dc == -1: base_angle = 180
            else: base_angle = 0
            
            angle1 = math.radians(base_angle - mouth_angle)
            angle2 = math.radians(base_angle + mouth_angle)
            
            p1 = (center[0] + math.cos(angle1) * (r + 4), center[1] + math.sin(angle1) * (r + 4))
            p2 = (center[0] + math.cos(angle2) * (r + 4), center[1] + math.sin(angle2) * (r + 4))
            
            pygame.draw.polygon(pac_surf, (1, 1, 1), [center, p1, p2])
            
        surface.blit(pac_surf, (cx - center[0], cy - center[1]))

class Ghost(Entity):
    """
    AI-controlled hostile entities.
    
    Ghosts use pathfinding algorithms (BFS or Random Walk) to navigate the grid.
    
    Attributes:
        is_hard_mode (bool): Whether to use BFS for intelligent tracking.
    """
    def __init__(self, r, c, color, is_hard_mode=False, ghost_type="Blinky"):
        """
        Initializes a Ghost with its specific AI behavior and start position.
        
        Args:
            r (int): Starting row index.
            c (int): Starting column index.
            color (tuple): RGB color representation.
            is_hard_mode (bool): Enables BFS pathfinding targeting.
            ghost_type (str): Type of the ghost affecting its behavior (e.g., 'Blinky', 'Pinky').
        """
        super().__init__(r, c, color)
        self.is_hard_mode = is_hard_mode
        self.ghost_type = ghost_type
        self.move_delay = 22 # Move every 22 frames
        self.move_timer = 0
        self.frightened_timer = 0
        self.is_dead = False
        self.respawn_timer = 0
        self.dr = 0
        self.dc = 0
        self.start_r = r
        self.start_c = c
        
    def frighten(self):
        """Puts the ghost into a frightened state where it moves slower and can be eaten."""
        if not self.is_dead:
            self.frightened_timer = FPS * 4 # 4 seconds of frightened state
        
    def die(self):
        """Handles the ghost's death, turning it into eyes and forcing it to return to spawn."""
        self.is_dead = True
        self.frightened_timer = 0
        
    def update(self, pacman, grid, other_ghosts):
        """
        Ghost AI behavior loop.
        
        Calculates the next position based on the chosen pathfinding algorithm
        and prevents ghosts from overlapping at the same grid cell.
        
        Args:
            pacman (Pacman): The player character.
            grid (list[list[str]]): The game grid matrix.
            other_ghosts (list[Ghost]): List of all ghost entities for collision avoidance.
        """
        import algorithms
        
        if self.is_dead:
            if self.respawn_timer > 0:
                self.respawn_timer -= 1
                if self.respawn_timer % (FPS // 4) == 0:
                    import random
                    self.dr, self.dc = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                if self.respawn_timer <= 0:
                    self.is_dead = False
                return
                
            # Fleeing back to spawn point
            self.move_timer += 2 # Move faster when dead
            if self.move_timer >= self.move_delay:
                self.move_timer = 0
                next_pos = algorithms.bfs_shortest_path((self.r, self.c), (self.start_r, self.start_c), grid)
                if next_pos:
                    self.r, self.c = next_pos
                if self.r == self.start_r and self.c == self.start_c:
                    self.respawn_timer = FPS * 3 # 3 seconds delay at spawn
            return

        if self.frightened_timer > 0:
            self.frightened_timer -= 1
            
        self.move_timer += 1
        # Frightened ghosts move slower
        current_delay = self.move_delay * 2.0 if self.frightened_timer > 0 else self.move_delay
        
        if self.move_timer >= current_delay:
            self.move_timer = 0
            
            # Determine Pathfinding strategy based on Difficulty Setting
            current_pos = (self.r, self.c)
            occupied = set((g.r, g.c) for g in other_ghosts if g != self) # Collision bounding
            
            import algorithms
            import random
            
            if self.frightened_timer > 0:
                # Frightened ghosts move randomly
                next_pos = algorithms.random_walk_algorithm(current_pos, grid, occupied_positions=occupied)
            else:
                target_pos = (pacman.r, pacman.c)
                
                # If hard mode, use type-specific AI logic for target cell
                if self.is_hard_mode:
                    if self.ghost_type == "Pinky":
                        # Target 4 tiles ahead of Pac-Man
                        target_pos = (pacman.r + pacman.dr * 4, pacman.c + pacman.dc * 4)
                    elif self.ghost_type == "Clyde":
                        # Instead of scattering (which looks like he's still frightened/running away),
                        # make him target Pacman directly or just slightly behind to avoid confusion.
                        target_pos = (pacman.r, pacman.c)
                
                # BFS Target tracking for both modes to prevent random "frightened-like" stumbling
                if self.is_hard_mode:
                    next_pos = bfs_shortest_path(current_pos, target_pos, grid, occupied_positions=occupied)
                else:
                    # Easy AI: Chase but without type-specific advanced targeting (just follows Pacman)
                    # We removed the 25% random walk so they don't look "frightened" when they recover
                    next_pos = bfs_shortest_path(current_pos, target_pos, grid, occupied_positions=occupied)
                
            # Apply movement
            if next_pos:
                # Update direction for rendering
                d_r = next_pos[0] - self.r
                d_c = next_pos[1] - self.c
                
                # Handle tunnel wrapping difference
                if d_c > 1: d_c = -1
                elif d_c < -1: d_c = 1
                
                if d_r != 0 or d_c != 0:
                    self.dr = d_r
                    self.dc = d_c
                
                # Tunnel wrap around for ghosts too
                nr, nc = next_pos
                if nc < 0: nc = COLS - 1
                elif nc >= COLS: nc = 0
                self.r, self.c = nr, nc

    def draw(self, surface):
        """Overrides base Entity draw for classic Ghost shape."""
        x = self.c * CELL_SIZE
        y = self.r * CELL_SIZE + UI_OFFSET_Y
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        r = CELL_SIZE // 2 - 2
        
        # Eyes sizes
        eye_r = int(r // 2.5)
        pupil_r = int(eye_r // 2)
        eye_y = int(cy - r // 4)
        
        # Eye offsets based on facing direction
        eye_offset_x = self.dc * 2
        eye_offset_y = self.dr * 2
        
        left_eye_x = int(cx - eye_r*1.1) + eye_offset_x
        right_eye_x = int(cx + eye_r*1.1) + eye_offset_x
        eye_y = int(cy - r // 4) + eye_offset_y
        
        pupil_offset_x = self.dc * 2
        pupil_offset_y = self.dr * 2

        # If dead, only draw eyes (unless respawning in base)
        if self.is_dead and self.respawn_timer == 0:
            pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), eye_r)
            pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), eye_r)
            pygame.draw.circle(surface, BLUE, (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_r)
            pygame.draw.circle(surface, BLUE, (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_r)
            return
        
        # Color logic for frightened state
        if self.frightened_timer > 0:
            # Flash white and red near the end of the timer
            is_flashing = self.frightened_timer < FPS * 3 and (self.frightened_timer // (FPS // 4)) % 2 == 0
            if is_flashing:
                current_color = WHITE
                face_color = RED
            else:
                current_color = (0, 0, 200) # Dark blue, a bit more vibrant
                face_color = (255, 184, 174) # Peach
        else:
            current_color = self.color
            face_color = None
            
        # Draw glowing aura for ghosts too!
        glow = get_glow_surface(current_color, r)
        surface.blit(glow, (cx - r*2, cy - r*2))
        
        # Dome top
        pygame.gfxdraw.aacircle(surface, cx, cy, r, current_color)
        pygame.gfxdraw.filled_circle(surface, cx, cy, r, current_color)
        
        # Boxy body + wavy legs
        time_ms = pygame.time.get_ticks()
        phase_offset = self.start_c * 10
        leg_wave = math.sin(time_ms * 0.01 + phase_offset) * 2

        points = [
            (cx - r, cy),               
            (cx + r, cy),               
            (cx + r, cy + r + leg_wave),           
            (cx + r/3.0, cy + r - 4 - leg_wave),   
            (cx, cy + r + leg_wave),               
            (cx - r/3.0, cy + r - 4 - leg_wave),   
            (cx - r, cy + r + leg_wave)            
        ]
        pygame.draw.polygon(surface, current_color, points)
        
        if self.frightened_timer > 0:
            # Frightened eyes
            pygame.draw.circle(surface, face_color, (left_eye_x, eye_y), pupil_r)
            pygame.draw.circle(surface, face_color, (right_eye_x, eye_y), pupil_r)
            
            # Wavy mouth
            mouth_y = int(cy + r // 4)
            mouth_w = r * 1.2
            mx = cx - mouth_w // 2
            mouth_points = [
                (mx, mouth_y + 2),
                (mx + mouth_w//4, mouth_y - 2),
                (mx + 2*mouth_w//4, mouth_y + 2),
                (mx + 3*mouth_w//4, mouth_y - 2),
                (mx + mouth_w, mouth_y + 2)
            ]
            pygame.draw.lines(surface, face_color, False, mouth_points, 2)
        else:
            # Sclera (White part)
            pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), eye_r)
            pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), eye_r)
            
            # Pupils (Blue part)
            pygame.draw.circle(surface, BLUE, (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_r)
            pygame.draw.circle(surface, BLUE, (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_r)
