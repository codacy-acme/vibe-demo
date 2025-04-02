import pygame
import sys
from enum import Enum
from typing import Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class GameState(Enum):
    MENU = 0
    SNAKE = 1
    TETRIS = 2


class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake & Tetris")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.current_game: Optional[object] = None
        self.font = pygame.font.Font(None, 74)

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    from snake_game import SnakeGame
                    self.current_game = SnakeGame(self)
                    self.state = GameState.SNAKE
                elif event.key == pygame.K_2:
                    from tetris_game import TetrisGame
                    self.current_game = TetrisGame(self)
                    self.state = GameState.TETRIS
                elif event.key == pygame.K_ESCAPE and self.current_game:
                    self.state = GameState.MENU

    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.font.render("Choose Your Game", True, WHITE)
        snake_option = self.font.render("1: Snake", True, GREEN)
        tetris_option = self.font.render("2: Tetris", True, BLUE)
        
        title_rect = title.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/4))
        snake_rect = snake_option.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
        tetris_rect = tetris_option.get_rect(center=(WINDOW_SIZE/2, 3*WINDOW_SIZE/4))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(snake_option, snake_rect)
        self.screen.blit(tetris_option, tetris_rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            if self.state == GameState.MENU:
                self.handle_menu_input()
                self.draw_menu()
            else:
                self.current_game.run_frame()
            
            self.clock.tick(FPS)


if __name__ == "__main__":
    manager = GameManager()
    manager.run() 