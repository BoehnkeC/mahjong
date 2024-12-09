import pygame
import pytest

from mahjong.positioner import NoneTouching
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
def tiles_none_touching(screen, tiles) -> Tiles:
    tiles.get_tiles(positions=NoneTouching.positions, draw=True)
    return tiles


def select_ul_tile(event, tile) -> Tile:
    event.pos = (tile.x_offset + tile.width / 2, tile.y_offset + tile.height / 2)
    return event


def test_1_tile(tiles_none_touching) -> None:
    """Test if a tile was selected."""
    tile = tiles_none_touching.tiles[0]
    assert tile.color == RED
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    select_ul_tile(event, tile)
    tile.check_event(event)

    assert tile.color == GREEN
