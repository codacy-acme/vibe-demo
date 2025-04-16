import pytest
import pygame
from unittest.mock import Mock, patch
from snake_game import SnakeGame

@pytest.fixture
def snake_game():
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'):
        game = SnakeGame()
        yield game
        pygame.quit()

def test_init(snake_game):
    assert snake_game.width == 800
    assert snake_game.height == 600
    assert snake_game.running is True
    assert len(snake_game.snake_body) > 0
    assert snake_game.direction == [0, 0]
    assert isinstance(snake_game.food_pos, list)

def test_spawn_food(snake_game):
    with patch('random.randrange', side_effect=[100, 100]):
        snake_game.spawn_food()
        assert snake_game.food_pos == [100, 100]

def test_move_snake(snake_game):
    initial_pos = snake_game.snake_body[0].copy()
    snake_game.direction = [1, 0]  # Move right
    snake_game.move_snake()
    new_pos = snake_game.snake_body[0]
    assert new_pos[0] == initial_pos[0] + 20  # Grid size is 20
    assert new_pos[1] == initial_pos[1]

@pytest.mark.parametrize("key,expected_direction", [
    (pygame.K_UP, [0, -1]),
    (pygame.K_DOWN, [0, 1]),
    (pygame.K_LEFT, [-1, 0]),
    (pygame.K_RIGHT, [1, 0]),
])
def test_handle_keys(snake_game, key, expected_direction):
    event = Mock(type=pygame.KEYDOWN, key=key)
    snake_game.handle_keys(event)
    assert snake_game.direction == expected_direction

def test_check_collision_with_walls(snake_game):
    # Test collision with right wall
    snake_game.snake_body[0] = [snake_game.width, snake_game.height//2]
    assert snake_game.check_collision()
    
    # Test collision with bottom wall
    snake_game.snake_body[0] = [snake_game.width//2, snake_game.height]
    assert snake_game.check_collision()

def test_check_collision_with_self(snake_game):
    # Create a scenario where snake collides with itself
    snake_game.snake_body = [[100, 100], [100, 100]]
    assert snake_game.check_collision()

def test_eat_food(snake_game):
    snake_game.food_pos = snake_game.snake_body[0].copy()
    initial_length = len(snake_game.snake_body)
    snake_game.check_food()
    assert len(snake_game.snake_body) == initial_length + 1

def test_run_game_loop(snake_game):
    events = [
        Mock(type=pygame.KEYDOWN, key=pygame.K_UP),
        Mock(type=pygame.QUIT)
    ]
    with patch('pygame.event.get', return_value=events), \
         patch('pygame.time.Clock.tick'), \
         patch.object(snake_game, 'draw'):
        snake_game.run()
        assert not snake_game.running 