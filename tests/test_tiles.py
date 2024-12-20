import pygame
import pytest

from mahjong.positioner import NoneTouching
from mahjong.rules import Rules
from mahjong.screen import Screen
from mahjong.tiles import Tile, Tiles

GREEN = (0, 255, 0)
RED = (255, 0, 0)


@pytest.fixture
def screen() -> pygame.Surface:
    return Screen()


@pytest.fixture
def tiles() -> Tiles:
    return Tiles()


@pytest.fixture
def rules() -> Rules:
    return Rules()


@pytest.fixture
def tiles_none_touching(screen, tiles) -> Tiles:
    tiles.get_tiles(positions=NoneTouching.positions, draw=True)
    return tiles


def get_tile(event, tile) -> Tile:
    event.pos = (tile.x_offset + tile.width / 2, tile.y_offset + tile.height / 2)
    return event


def test_1_tile_selected(tiles_none_touching) -> None:
    """Test if a tile was selected.
    Simulate a mouse event at the tile center coordinates."""
    tile = tiles_none_touching.tiles[0]
    assert not tile.selected
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    get_tile(event, tile)  # select upper left tile
    tile.check_clicked(event)

    assert tile.selected


def test_2_tiles_selected(tiles_none_touching) -> None:
    """Test if 2 tiles were selected.
    Simulate a mouse event at the tile center coordinates."""
    for tile in tiles_none_touching.tiles[:2]:
        assert not tile.selected

    # simulate mouse click events at the center of the first 2 tiles
    for tile in tiles_none_touching.tiles[:2]:
        center_x, center_y = tile.outline.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (center_x, center_y)})
        tiles_none_touching.check_event(event)

    # check if the first 2 tiles are selected
    for tile in tiles_none_touching.tiles[:2]:
        assert tile.selected

    # check if the rest of the tiles are not selected
    for tile in tiles_none_touching.tiles[2:]:
        assert not tile.selected


def test_tiles_selected_limit(tiles_none_touching, rules) -> None:
    """Test broken rule when more than 2 tiles were selected.
    Simulate a mouse event at the tile center coordinates."""
    for tile in tiles_none_touching.tiles[:2]:
        assert not tile.selected

    # simulate mouse click events at the center of the first 3 tiles
    for i, tile in enumerate(tiles_none_touching.tiles[:3]):
        center_x, center_y = tile.outline.center
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (center_x, center_y)})
        tiles_none_touching.check_event(event)
        tiles_none_touching.check_rules()

        if i < 2:
            assert len(tiles_none_touching.selected_tiles) < 3
            assert not tile.rules.broken

    # check if the rest of the tiles are not selected
    for tile in tiles_none_touching.tiles:
        assert not tile.selected
