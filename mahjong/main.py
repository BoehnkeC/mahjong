from collections.abc import Generator
from pathlib import Path

import pygame
from pydantic import BaseModel

GREY = (200, 200, 200)
RED = (255, 0, 0)


class Parameters(BaseModel):
    tile_width: int = 50
    tile_height: int = int(tile_width * 1.5)
    num_pairs: int = 2
    num_tiles: int = num_pairs * 2
    x_offset: int = 50  # space between left/right edge and tile
    y_offset: int = 50  # space between top/bottom edge and tile
    x_space: int = 20  # space between tiles in x direction
    y_space: int = 20  # space between tiles in y direction
    rows: int = num_pairs  # number of rows
    cols: int = 2  # number of columns
    canvas_width: int = x_offset * 2 + tile_width * cols + x_space * (cols - 1)
    canvas_height: int = y_offset * 2 + tile_height * rows + y_space * (rows - 1)


class Game:
    def __init__(self) -> None:
        self.params = Parameters()
        pygame.init()

    def __enter__(self) -> "Game":
        return self

    def __exit__(self, *args) -> None:
        pygame.quit()

    def event_loop(self, running: bool = True) -> Generator[bool, None, None]:
        """Event loop handling user interactions."""
        while running:  # game still running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if quit button is pressed
                    running = False  # stop the game

            yield running


class Tiles:
    def __init__(self) -> None:
        self.params = Parameters()
        self.get_tiles()

    def get_tiles(self) -> None:
        self.tiles: list[Tile] = []

        for col in range(self.params.cols):
            for row in range(self.params.rows):
                self.tiles.append(
                    Tile(
                        self.params.x_offset + (self.params.tile_width + self.params.x_space) * col,
                        self.params.y_offset + (self.params.tile_height + self.params.y_space) * row,
                    )
                )


class Tile:
    def __init__(self, x_offset: int, y_offset: int) -> None:
        self.params = Parameters()
        self.color = RED
        self.img = pygame.image.load(Path(Path(__file__).parent.parent.joinpath("tiles", "Chun.png")))
        self.img.convert()
        self.img = pygame.transform.scale(self.img, (self.params.tile_width, self.params.tile_height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x_offset, y_offset)


class Screen:
    def __init__(self) -> None:
        self.params = Parameters()
        self.get_screen()
        self.draw_background()

    def get_screen(self, size: tuple[int, int] = (800, 600)) -> None:
        self.screen = pygame.display.set_mode((self.params.canvas_width, self.params.canvas_height))

    def draw_background(self) -> None:
        self.screen.fill(GREY)

    def draw_tile(self, tile: Tile) -> None:
        pygame.draw.rect(self.screen, tile.color, tile.rect, 1)
        self.screen.blit(tile.img, tile.rect)


if __name__ == "__main__":
    with Game() as game:
        screen = Screen()
        tiles = Tiles()

        for _ in game.event_loop():
            screen.draw_background()
            for tile in tiles.tiles:
                screen.draw_tile(tile)
            pygame.display.update()  # update the screen to show the color
