import pygame
import random
import sys
import numpy as np

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.grid_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.COLORS = [
            (0, 255, 255),  # I piece
            (255, 255, 0),  # O piece
            (128, 0, 128),  # T piece
            (0, 255, 0),    # S piece
            (255, 0, 0),    # Z piece
            (0, 0, 255),    # J piece
            (255, 165, 0),  # L piece
        ]
        
        # Tetromino shapes
        self.SHAPES = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[0, 1, 0], [1, 1, 1]],  # T
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 0], [0, 1, 1]],  # Z
            [[1, 0, 0], [1, 1, 1]],  # J
            [[0, 0, 1], [1, 1, 1]],  # L
        ]
        
        self.reset_game()
        
    def reset_game(self):
        self.board = np.zeros((self.grid_height, self.grid_width))
        self.score = 0
        self.game_over = False
        self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 500  # Time in milliseconds
        
    def spawn_piece(self):
        # Choose random shape
        shape_idx = random.randint(0, len(self.SHAPES) - 1)
        self.current_piece = np.array(self.SHAPES[shape_idx])
        self.current_color = self.COLORS[shape_idx]
        
        # Starting position
        self.piece_x = self.grid_width // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        
        # Check if piece can be placed
        if not self.valid_move(self.piece_y, self.piece_x, self.current_piece):
            self.game_over = True
    
    def valid_move(self, y, x, piece):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] == 0:
                    continue
                    
                new_y = y + i
                new_x = x + j
                
                if (new_x < 0 or new_x >= self.grid_width or
                    new_y >= self.grid_height or
                    (new_y >= 0 and self.board[new_y][new_x] != 0)):
                    return False
        return True
    
    def rotate_piece(self):
        rotated_piece = np.rot90(self.current_piece, -1)
        if self.valid_move(self.piece_y, self.piece_x, rotated_piece):
            self.current_piece = rotated_piece
    
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
                    
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.piece_y, self.piece_x - 1, self.current_piece):
                            self.piece_x -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.valid_move(self.piece_y, self.piece_x + 1, self.current_piece):
                            self.piece_x += 1
                    if event.key == pygame.K_DOWN:
                        if self.valid_move(self.piece_y + 1, self.piece_x, self.current_piece):
                            self.piece_y += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    if event.key == pygame.K_SPACE:
                        while self.valid_move(self.piece_y + 1, self.piece_x, self.current_piece):
                            self.piece_y += 1
        return True
    
    def update(self):
        if self.game_over:
            return
            
        # Update fall time
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if self.valid_move(self.piece_y + 1, self.piece_x, self.current_piece):
                self.piece_y += 1
            else:
                # Lock piece in place
                for i in range(len(self.current_piece)):
                    for j in range(len(self.current_piece[0])):
                        if self.current_piece[i][j] == 1:
                            self.board[self.piece_y + i][self.piece_x + j] = 1
                
                # Check for completed lines
                lines_cleared = 0
                for i in range(self.grid_height):
                    if np.all(self.board[i]):
                        lines_cleared += 1
                        # Move all lines above down
                        self.board = np.vstack((np.zeros(self.grid_width), self.board[:i], self.board[i+1:]))
                
                # Update score
                self.score += lines_cleared * 100
                
                # Spawn new piece
                self.spawn_piece()
    
    def draw_grid(self):
        # Draw board
        board_surface = pygame.Surface((self.grid_width * self.grid_size, self.grid_height * self.grid_size))
        board_surface.fill(self.BLACK)
        
        # Draw grid lines
        for x in range(self.grid_width):
            pygame.draw.line(board_surface, self.WHITE, (x * self.grid_size, 0),
                           (x * self.grid_size, self.grid_height * self.grid_size))
        for y in range(self.grid_height):
            pygame.draw.line(board_surface, self.WHITE, (0, y * self.grid_size),
                           (self.grid_width * self.grid_size, y * self.grid_size))
        
        # Draw locked pieces
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(board_surface, self.WHITE,
                                   (x * self.grid_size, y * self.grid_size,
                                    self.grid_size-1, self.grid_size-1))
        
        # Draw current piece
        if not self.game_over:
            for i in range(len(self.current_piece)):
                for j in range(len(self.current_piece[0])):
                    if self.current_piece[i][j] == 1:
                        pygame.draw.rect(board_surface, self.current_color,
                                       ((self.piece_x + j) * self.grid_size,
                                        (self.piece_y + i) * self.grid_size,
                                        self.grid_size-1, self.grid_size-1))
        
        # Center the board on screen
        board_x = (self.width - self.grid_width * self.grid_size) // 2
        board_y = (self.height - self.grid_height * self.grid_size) // 2
        self.screen.blit(board_surface, (board_x, board_y))
    
    def draw(self):
        self.screen.fill(self.BLACK)
        self.draw_grid()
        
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
            self.clock.tick(60) 