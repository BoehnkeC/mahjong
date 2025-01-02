import pygame

from .parameters import Parameters
from .tiles import Tile, Tiles

GREY = (200, 200, 200)


class Screen:
    def __init__(self, positions: object) -> None:
        self.params = Parameters()
        self.positions: object = positions
        self.get_screen_geometry()
        self.get_screen()
        self.draw_background()
        self.get_rectangle()
        self.selected: bool = False

    def get_screen_geometry(self) -> None:
        self.canvas_width: int = self.params.x_offset * 2 + self.params.tile_width * self.positions.cols
        self.canvas_height: int = self.params.y_offset * 2 + self.params.tile_height * self.positions.rows

    def get_screen(self) -> None:
        self.screen = pygame.display.set_mode((self.canvas_width, self.canvas_height))

    def draw_background(self) -> None:
        self.screen.fill(GREY)

    def draw_tile(self, tile: Tile) -> None:
        self.draw_tile_outline(tile)
        self.draw_tile_face(tile)

    def draw_tile_outline(self, tile: Tile) -> None:
        pygame.draw.rect(self.screen, tile.color, tile.outline, 1, 5)

    def draw_tile_face(self, tile: Tile) -> None:
        self.screen.blit(tile.face, tile.outline)

    def draw_tile_overlay(self, tiles: Tiles) -> None:
        """Tile was selected and gets a transparent yellow overlay."""
        for tile in tiles:
            if tile.selected:
                self.screen.blit(tile.overlay, tile.outline.topleft)

    def get_rectangle(self) -> None:
        self.rectangle = self.screen.get_rect()

    def check_event(self, event: pygame.event.Event, tiles: Tiles) -> None:
        """Check if the screen instead of a tile was selected.
        It follows the same logic as for the tile selection, keeping continuity."""
        if self.check_clicked(event, tiles):
            tiles.deselect()  # deselect all tiles as screen has been selected

    def check_clicked(self, event: pygame.event.Event, tiles: Tiles) -> bool:
        """Check if the screen was selected through a mouse button event."""
        if self.rectangle.collidepoint(event.pos) and not any(
            [tile.outline.collidepoint(event.pos) for tile in tiles.tiles]
        ):
            self.selected = True
            print("Selected screen")
            return True
