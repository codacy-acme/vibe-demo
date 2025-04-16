import pytest
import pygame
from unittest.mock import Mock, patch
from game_selector import GameSelector

@pytest.fixture
def game_selector():
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'):
        selector = GameSelector()
        yield selector
        pygame.quit()

def test_init(game_selector):
    assert game_selector.width == 800
    assert game_selector.height == 600
    assert game_selector.running is True

def test_draw_menu(game_selector):
    with patch('pygame.font.Font'), \
         patch('pygame.Surface'), \
         patch('pygame.display.update'):
        game_selector.draw_menu()
        # Test passes if no exceptions are raised

@pytest.mark.parametrize("mouse_pos,expected_game", [
    ((400, 250), "snake"),  # Snake button position
    ((400, 350), "tetris"),  # Tetris button position
    ((400, 500), None),  # No button position
])
def test_handle_click(game_selector, mouse_pos, expected_game):
    with patch('pygame.mouse.get_pos', return_value=mouse_pos):
        result = game_selector.handle_click()
        assert result == expected_game

def test_run(game_selector):
    events = [
        Mock(type=pygame.MOUSEBUTTONDOWN),
        Mock(type=pygame.QUIT)
    ]
    with patch('pygame.event.get', return_value=events), \
         patch('pygame.time.Clock.tick'), \
         patch.object(game_selector, 'handle_click', return_value=None), \
         patch.object(game_selector, 'draw_menu'):
        game_selector.run()
        assert not game_selector.running 