import pygame
import random
import sys

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.grid_size = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        
        self.reset_game()
        
    def reset_game(self):
        # Snake initial position and direction
        self.snake = [(self.width//2, self.height//2)]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"
        
        # Food position
        self.spawn_food()
        
        # Score
        self.score = 0
        self.game_over = False
        
    def spawn_food(self):
        while True:
            x = random.randrange(self.grid_size, self.width - self.grid_size, self.grid_size)
            y = random.randrange(self.grid_size, self.height - self.grid_size, self.grid_size)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # Direction changes
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.new_direction = "UP"
                if event.key == pygame.K_DOWN and self.direction != "UP":
                    self.new_direction = "DOWN"
                if event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.new_direction = "LEFT"
                if event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.new_direction = "RIGHT"
        return True
    
    def update(self):
        if self.game_over:
            return
            
        # Update direction
        self.direction = self.new_direction
        
        # Get current head position
        x, y = self.snake[0]
        
        # Calculate new head position
        if self.direction == "UP":
            y -= self.grid_size
        elif self.direction == "DOWN":
            y += self.grid_size
        elif self.direction == "LEFT":
            x -= self.grid_size
        elif self.direction == "RIGHT":
            x += self.grid_size
            
        # Check collision with walls
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            self.game_over = True
            return
            
        # Check collision with self
        if (x, y) in self.snake:
            self.game_over = True
            return
            
        # Add new head
        self.snake.insert(0, (x, y))
        
        # Check if food is eaten
        if (x, y) == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.GREEN,
                           (segment[0], segment[1], self.grid_size-2, self.grid_size-2))
        
        # Draw food
        pygame.draw.rect(self.screen, self.RED,
                        (self.food[0], self.food[1], self.grid_size-2, self.grid_size-2))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('Game Over!', True, self.WHITE)
            restart_text = font.render('Press R to Restart', True, self.WHITE)
            self.screen.blit(game_over_text,
                           (self.width//2 - game_over_text.get_width()//2,
                            self.height//2 - game_over_text.get_height()//2))
            self.screen.blit(restart_text,
                           (self.width//2 - restart_text.get_width()//2,
                            self.height//2 + restart_text.get_height()))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            if not self.handle_input():
                break
                
            self.update()
            self.draw()
            self.clock.tick(10)  # Control game speed 