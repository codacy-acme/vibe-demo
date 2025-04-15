import pygame
import sys
from snake_game import SnakeGame
from tetris_game import TetrisGame

class GameSelector:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Selector")
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        # Title
        title = self.font.render("Choose Your Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width/2, 100))
        self.screen.blit(title, title_rect)
        
        # Snake button
        snake_text = self.font.render("Snake", True, (0, 255, 0))
        snake_rect = snake_text.get_rect(center=(self.width/2, 250))
        self.screen.blit(snake_text, snake_rect)
        
        # Tetris button
        tetris_text = self.font.render("Tetris", True, (0, 255, 255))
        tetris_rect = tetris_text.get_rect(center=(self.width/2, 400))
        self.screen.blit(tetris_text, tetris_rect)
        
        # Instructions
        instructions = self.small_font.render("Click on a game to start", True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(self.width/2, 500))
        self.screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Snake button click detection
                    snake_rect = pygame.Rect(self.width/2 - 100, 220, 200, 60)
                    if snake_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        snake_game = SnakeGame()
                        snake_game.run()
                        pygame.init()
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        
                    # Tetris button click detection
                    tetris_rect = pygame.Rect(self.width/2 - 100, 370, 200, 60)
                    if tetris_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        tetris_game = TetrisGame()
                        tetris_game.run()
                        pygame.init()
                        self.screen = pygame.display.set_mode((self.width, self.height))
            
            self.draw_menu()

if __name__ == "__main__":
    selector = GameSelector()
    selector.run() 