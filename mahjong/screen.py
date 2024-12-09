import pygame

from .parameters import Parameters
from .tiles import Tile

GREY = (200, 200, 200)


class Screen:
    def __init__(self) -> None:
        self.params = Parameters()
        self.get_screen()
        self.draw_background()

    def get_screen(self) -> None:
        self.screen = pygame.display.set_mode((self.params.canvas_width, self.params.canvas_height))

    def draw_background(self) -> None:
        self.screen.fill(GREY)

    def draw_tile(self, tile: Tile) -> None:
        self.draw_tile_outline(tile)
        self.draw_tile_face(tile)

    def draw_tile_outline(self, tile: Tile) -> None:
        pygame.draw.rect(self.screen, tile.color, tile.outline, 1, 5)

    def draw_tile_face(self, tile: Tile) -> None:
        self.screen.blit(tile.face, tile.outline)
