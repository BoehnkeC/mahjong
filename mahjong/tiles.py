import pygame

from .parameters import Parameters
from .rules import Rules

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Tiles:
    def __init__(self) -> None:
        self.tiles: list[Tile] | None = None
        self.selected: int = 0  # number of selected tiles, must nood exceed selection limit of 2

    def get_tiles(self, positions: list, draw: bool = True) -> None:
        """Create tiles at pre-defined tile positions."""
        self.tiles = [Tile(i, *p, draw=draw) for i, p in enumerate(positions)]


class Tile:
    def __init__(self, index: int, x_offset: int, y_offset: int, draw: bool = True) -> None:
        self.params = Parameters()
        self.id = index
        self.x_offset: int = x_offset
        self.y_offset: int = y_offset
        self.width: int = self.params.tile_width
        self.height: int = self.params.tile_height
        self.color = RED  # use background color to have frame color seem transparent
        self.selected = False
        self.rules = Rules()  # rule set applies per tile

        if draw:
            self.get_face()
            self.get_outline()

    def get_face(self) -> None:
        """Get the tile face, i.e. a drawable area entity."""
        self.face = pygame.image.load(self.params.tiles_path.joinpath("Front.png"))
        self.face.convert()  # optimize image format and make drawing faster
        self.face = pygame.transform.scale(self.face, (self.width, self.height))

    def get_outline(self) -> None:
        """Get outline coordinates of the tile."""
        self.outline = self.face.get_rect()
        self.outline.topleft = (self.x_offset, self.y_offset)

    def check_event(self, event: pygame.event.Event) -> None:
        """Check if the mouse button was pressed.
        Select the tile if the position is within the tile bounding box."""
        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse button is pressed
            x, y = event.pos  # get x and y position of mouse click

            if self.outline.collidepoint(x, y):
                self.selected = True

    def check_rules(self, num_selected: int) -> int:
        """Check if the tile can be selected based on the rules."""
        if self.selected:
            num_selected += 1
            self.rules.check_rules(num_selected)

            if self.rules.broken:
                print(self.rules.reason)

        return num_selected
