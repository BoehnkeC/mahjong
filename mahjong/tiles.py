import pygame

from .parameters import Parameters
from .rules import Distribution, Rules

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Tiles:
    def __init__(self) -> None:
        self.tiles: list[Tile] | None = None
        self.rules = Rules()  # rule set applies per tiles
        self.selected_tiles: list = []

    def init_tiles(self, positions: object, draw: bool = True) -> None:
        """Create tiles at pre-defined tile positions."""
        # loop over tile positions with positions.positions
        # looop over tile faces with positions.faces
        # unpack positions with *p[0] and faces with p[1]
        self.tiles = [Tile(i, *p[0], p[1]) for i, p in enumerate(zip(positions.positions, positions.faces))]

    def check_event(self, event: pygame.event.Event):
        """Check if a tile was selected through a mouse button event."""
        for tile in self.tiles:
            if tile.check_clicked(event):  # tile was clicked
                if tile.selected:  # tile got clicked and selected
                    self.selected_tiles.append(tile)

                    # due to the way events are handled, the selected tiles are appended multiple times
                    self.selected_tiles = list(dict.fromkeys(self.selected_tiles))
                    self.rules.check_rules(self.selected_tiles)

                else:  # tile got clicked but deselected
                    self.selected_tiles.remove(tile)

    def apply_rules(self) -> None:
        """Apply the rules to the selected tiles. Rules have been checked before."""
        if self.rules.broken:
            if self.rules.reason == Distribution.limit:
                self.deselect()

            elif self.rules.reason == Distribution.pair:
                self.selected_tiles[0].deselect()
                self.selected_tiles.remove(self.selected_tiles[0])

        else:
            if len(self.selected_tiles) == 2:
                self.remove()

        self.rules.broken = False

    def deselect(self) -> None:
        """Deselect all tiles."""
        for tile in reversed(self.selected_tiles):
            tile.deselect()
            self.selected_tiles.remove(tile)

    def remove(self) -> None:
        """Remove selected pair of tiles from the game."""
        for i in range(2):
            self.tiles.remove(self.tiles[self.tiles.index(self.selected_tiles[i])])

        self.deselect()


class Tile:
    def __init__(self, index: int, x_offset: int, y_offset: int, face: str, draw: bool = True) -> None:
        self.params = Parameters()
        self.id = index
        self.name: str | None = None  # name of the tile, equivalent to the image file name
        self.x_offset: int = x_offset
        self.y_offset: int = y_offset
        self.width: int = self.params.tile_width
        self.height: int = self.params.tile_height
        self.color = RED  # use background color to have frame color seem transparent
        self.selected = False  # selection is a persistent state until deselection

        if draw:
            self.get_face(face)
            self.overlay()
            self.get_outline()

    def get_face(self, face: str) -> None:
        """Get the tile face, i.e. a drawable area entity."""
        # load image and optimize with convert
        self.face = pygame.image.load(self.params.tiles_path.joinpath(f"{face}.png"))
        self.face = self.face.convert_alpha()
        self.face = pygame.transform.scale(self.face, (self.width, self.height))
        self.name = face

    def overlay(self) -> None:
        """Get the tiles transparent overlay used for selection."""
        self.overlay = pygame.Surface(self.face.get_size(), pygame.SRCALPHA, 32)
        self.overlay = self.overlay.convert_alpha()
        self.overlay.fill((255, 255, 81, 120))

    def get_outline(self) -> None:
        """Get outline coordinates of the tile."""
        self.outline = self.face.get_rect()
        self.outline.topleft = (self.x_offset, self.y_offset)

    def check_clicked(self, event: pygame.event.Event) -> bool:
        """Check if the mouse button was pressed.
        Select the tile if the position is within the tile bounding box and the tile has not been selected before.
        If the tile has been selected before, deselect it."""
        if not self.selected and self.outline.collidepoint(event.pos):
            self.selected = True
            return True  # return True because tile was clicked

        elif self.selected and self.outline.collidepoint(event.pos):
            self.deselect()
            return True  # return True because tile was clicked

    def deselect(self) -> None:
        self.selected = False
