import pygame
import random
from typing import List, Tuple

# Constants
WINDOW_SIZE = 800
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (WINDOW_SIZE - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = (WINDOW_SIZE - GRID_HEIGHT * BLOCK_SIZE) // 2
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class TetrisGame:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.fall_time = 0
        self.fall_speed = 0.5  # Time in seconds between automatic falls
        self.last_fall = pygame.time.get_ticks()

    def reset_game(self):
        """Reset the game state."""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.spawn_piece()

    def spawn_piece(self):
        """Create a new tetromino at the top of the grid."""
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }
        
        # Check if the new piece overlaps with existing blocks
        if self.check_collision():
            self.game_over = True

    def check_collision(self) -> bool:
        """Check if current piece collides with anything."""
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_piece['x'] + x
                    grid_y = self.current_piece['y'] + y
                    
                    if (grid_x < 0 or grid_x >= GRID_WIDTH or
                        grid_y >= GRID_HEIGHT or
                        (grid_y >= 0 and self.grid[grid_y][grid_x])):
                        return True
        return False

    def rotate_piece(self):
        """Rotate the current piece clockwise."""
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = list(zip(*reversed(old_shape)))
        
        # If rotation causes collision, revert
        if self.check_collision():
            self.current_piece['shape'] = old_shape

    def handle_input(self):
        """Handle keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.state = self.manager.GameState.MENU
                elif not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision():
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision():
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision():
                            self.current_piece['y'] -= 1
                elif event.key == pygame.K_r:
                    self.reset_game()

    def lock_piece(self):
        """Lock the current piece in place and spawn a new one."""
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece['y'] + y
                    if grid_y >= 0:  # Only place if within grid
                        self.grid[grid_y][self.current_piece['x'] + x] = self.current_piece['color']
        
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        """Clear any complete lines and update score."""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                # Move all lines above down
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                self.grid[0] = [0] * GRID_WIDTH
            else:
                y -= 1
        
        if lines_cleared:
            self.score += (lines_cleared * 100) * lines_cleared  # Bonus for multiple lines

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall > self.fall_speed * 1000:
            self.current_piece['y'] += 1
            if self.check_collision():
                self.current_piece['y'] -= 1
                self.lock_piece()
            self.last_fall = current_time

    def draw(self):
        """Draw the game state."""
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                if color:
                    pygame.draw.rect(self.screen, color, (
                        GRID_OFFSET_X + x * BLOCK_SIZE,
                        GRID_OFFSET_Y + y * BLOCK_SIZE,
                        BLOCK_SIZE - 1,
                        BLOCK_SIZE - 1
                    ))

        # Draw current piece
        if not self.game_over:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece['color'], (
                            GRID_OFFSET_X + (self.current_piece['x'] + x) * BLOCK_SIZE,
                            GRID_OFFSET_Y + (self.current_piece['y'] + y) * BLOCK_SIZE,
                            BLOCK_SIZE - 1,
                            BLOCK_SIZE - 1
                        ))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw ESC hint
        esc_text = font.render('ESC: Menu', True, WHITE)
        self.screen.blit(esc_text, (WINDOW_SIZE - 150, 10))

        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render('Game Over!', True, WHITE)
            restart_text = font.render('Press R to Restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 50))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        # Draw grid border
        pygame.draw.rect(self.screen, WHITE, (
            GRID_OFFSET_X - 2,
            GRID_OFFSET_Y - 2,
            GRID_WIDTH * BLOCK_SIZE + 4,
            GRID_HEIGHT * BLOCK_SIZE + 4
        ), 2)

        pygame.display.flip()

    def run_frame(self):
        """Run a single frame of the game."""
        self.handle_input()
        self.update()
        self.draw()
        self.clock.tick(FPS) 