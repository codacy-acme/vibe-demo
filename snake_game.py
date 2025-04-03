import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """Reset the game state."""
        self.snake: List[Tuple[int, int]] = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def _get_random_position(self) -> Tuple[int, int]:
        """Generate a random position for game mechanics.
        
        This is a helper method that generates random coordinates for game mechanics only.
        The randomness here is not used for any security-critical operations, making
        random.randint perfectly suitable for this purpose.
        
        Returns:
            Tuple[int, int]: Random (x, y) coordinates within the game grid
        """
        # nosec B311 semgrep.random
        return (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))

    def generate_food(self) -> Tuple[int, int]:
        """Generate food at a random position.
        
        This method uses non-cryptographic random number generation which is
        perfectly suitable for game mechanics where security is not a concern.
        The randomness is used exclusively for gameplay variety and food placement.
        
        Returns:
            Tuple[int, int]: The (x, y) coordinates of the food on the game grid
        """
        while True:
            position = self._get_random_position()
            if position not in self.snake:
                return position

    def handle_input(self):
        """Handle keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif not self.game_over:
                    self._handle_movement(event.key)

    def _handle_movement(self, key):
        """Handle snake movement based on key press."""
        direction_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
        }
        if key in direction_map:
            new_direction = direction_map[key]
            # Prevent 180-degree turns
            if (self.direction.value[0] + new_direction.value[0] != 0 or
                    self.direction.value[1] + new_direction.value[1] != 0):
                self.direction = new_direction

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        # Calculate new head position
        head = self.snake[0]
        new_head = (
            (head[0] + self.direction.value[0]) % GRID_COUNT,
            (head[1] + self.direction.value[1]) % GRID_COUNT
        )

        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check for food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        """Draw the game state."""
        self.screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1
            ))

        # Draw food
        pygame.draw.rect(self.screen, RED, (
            self.food[0] * GRID_SIZE,
            self.food[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        ))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render('Game Over!', True, WHITE)
            restart_text = font.render('Press R to Restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 50))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 