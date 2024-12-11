import pygame

from .parameters import Parameters
from .rules import Rules

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Tiles:
    def __init__(self) -> None:
        self.tiles: list[Tile] | None = None
        # self.selected: int = 0  # number of selected tiles, must nood exceed selection limit of 2
        self.rules = Rules()  # rule set applies per tile
        self.selected_tiles: list = []

    def get_tiles(self, positions: list, draw: bool = True) -> None:
        """Create tiles at pre-defined tile positions."""
        self.tiles = [Tile(i, *p, draw=draw) for i, p in enumerate(positions)]

    def check_event(self, event: pygame.event.Event):
        # self.selected: int = 0
        for tile in self.tiles:
            tile.check_selected(event)

            if tile.selected:
                print(f"Selected {tile.x_offset, tile.y_offset}")
                self.selected_tiles.append(tile)

                # due to the way events are handled, the selected tiles are appended multiple times
                self.selected_tiles = list(dict.fromkeys(self.selected_tiles))
                self.rules.check_rules(len(self.selected_tiles))

            if self.rules.broken:
                print(self.rules.reason)

    def deselect(self) -> None:
        """Deselect all tiles."""
        for tile in self.tiles:
            tile.selected = False
            self.selected_tiles = []


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

    def check_selected(self, event: pygame.event.Event) -> None:
        """Check if the mouse button was pressed.
        Select the tile if the position is within the tile bounding box."""
        if self.outline.collidepoint(event.pos):
            self.selected = True
