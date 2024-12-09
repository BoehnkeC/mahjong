import sys
from collections.abc import Generator

import pygame
from parameters import Parameters
from positioner import NoneTouching

GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


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


class Game:
    def __init__(self) -> None:
        pygame.init()

    def __enter__(self) -> "Game":
        return self

    def __exit__(self, *args) -> None:
        pygame.quit()

    def close(self) -> None:
        pygame.quit()
        sys.exit()

    def event_loop(self, running: bool = True) -> Generator[bool, None, None]:
        """Event loop handling user interactions."""
        while running:  # game still running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if quit button is pressed
                    running = False  # stop the game

                yield event


class Event(Game):
    def __init__(self, event) -> None:
        self.event: pygame.event.Event = event

    def check_event_type(self, tile) -> None:
        if self.event.type == pygame.QUIT:  # if quit button is pressed
            self.close()  # stop the game

        if self.event.type == pygame.MOUSEBUTTONDOWN:  # if mouse button is pressed
            x, y = self.event.pos  # get x and y position of mouse click

            if tile.outline.collidepoint(x, y):
                print(f"Tile {tile.id} clicked")
                tile.color = GREEN


if __name__ == "__main__":
    with Game() as game:
        screen = Screen()
        tiles = Tiles()

        for e in game.event_loop():
            event = Event(e)
            screen.draw_background()
            for tile in tiles.tiles:
                screen.draw_tile(tile)
                event.check_event_type(tile)

            pygame.display.update()  # update the screen to show the color
