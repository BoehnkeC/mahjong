import sys

import pygame

from .positioner import NoneTouching
from .rules import Rules
from .screen import Screen
from .tiles import Tiles

GREY = (200, 200, 200)
GREEN = (0, 255, 0)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.event: pygame.event.Event | None = None
        self.running: bool = True

        self.screen = Screen()
        self.tiles = Tiles()
        self.rules = Rules()

    def __enter__(self) -> "Game":
        return self

    def __exit__(self, *args) -> None:
        pygame.quit()

    def close(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        self.tiles.get_tiles(positions=NoneTouching.positions)

        while self.running:
            self.draw_tiles()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse click
                    self.tiles.check_event(event)
                    self.tiles.check_rules()
                    print([tile.id for tile in self.tiles.selected_tiles])
                    self.screen.check_event(event, self.tiles.tiles)

            self.screen.draw_tile_overlay(self.tiles.selected_tiles)

            if self.screen.selected:
                self.tiles.deselect()  # deselect all tiles as screen has been selected

            pygame.display.update()  # update the screen to show the color

    def draw_tiles(self) -> None:
        for tile in self.tiles.tiles:
            self.screen.draw_tile(tile)


if __name__ == "__main__":
    with Game() as game:
        game.run()
