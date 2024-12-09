import sys

import pygame

from .positioner import NoneTouching
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                for tile in self.tiles.tiles:
                    tile.check_event(event)

            self.screen.draw_background()
            self.draw_tiles()
            pygame.display.update()  # update the screen to show the color

    def draw_tiles(self) -> None:
        for tile in self.tiles.tiles:
            self.screen.draw_tile(tile)


if __name__ == "__main__":
    with Game() as game:
        game.run()
