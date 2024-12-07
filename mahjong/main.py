from collections.abc import Generator

import pygame
from parameters import Parameters
from positioner import NoneTouching

GREY = (200, 200, 200)
RED = (255, 0, 0)


class Game:
    def __init__(self) -> None:
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
        self.get_tiles()

    def get_tiles(self) -> None:
        self.tiles: list[Tile] = [Tile(i, *p) for i, p in enumerate(NoneTouching.positions)]


class Tile:
    def __init__(self, index: int, x_offset: int, y_offset: int) -> None:
        self.params = Parameters()
        self.id = index
        self.x_offset: int = x_offset
        self.y_offset: int = y_offset
        self.width: int = self.params.tile_width
        self.height: int = self.params.tile_height
        self.color = RED  # use background color to have frame color seem transparent
        self.get_face()
        self.get_outline()

    def get_face(self) -> None:
        self.face = pygame.image.load(self.params.tiles_path.joinpath("Front.png"))
        self.face.convert()  # optimize image format and make drawing faster
        self.face = pygame.transform.scale(self.face, (self.width, self.height))

    def get_outline(self) -> None:
        self.outline = self.face.get_rect()
        self.outline.topleft = (self.x_offset, self.y_offset)


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
        pygame.draw.rect(self.screen, tile.color, tile.outline, 1, 5)
        self.screen.blit(tile.face, tile.outline)


if __name__ == "__main__":
    with Game() as game:
        screen = Screen()
        tiles = Tiles()

        for _ in game.event_loop():
            screen.draw_background()
            for tile in tiles.tiles:
                screen.draw_tile(tile)
            pygame.display.update()  # update the screen to show the color
