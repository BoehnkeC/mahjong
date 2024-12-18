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
            if tile.check_clicked(event):  # tile was clicked
                if tile.selected:  # tile got clicked and selected
                    self.selected_tiles.append(tile)

                    # due to the way events are handled, the selected tiles are appended multiple times
                    self.selected_tiles = list(dict.fromkeys(self.selected_tiles))
                    self.rules.check_rules(len(self.selected_tiles))

                else:  # tile got clicked but deselected
                    print(f"Tile {tile.id} got clicked and gets deselected now.")
                    self.selected_tiles.remove(tile)

            # else:  # tile was selected before and is now deselected
            #     if tile in self.selected_tiles:
            #         self.selected_tiles.remove(tile)

    def check_rules(self) -> None:
        if self.rules.broken:
            self.deselect()
            print(self.rules.reason)

        self.rules.broken = False

    def deselect(self) -> None:
        """Deselect all tiles."""
        for tile in self.tiles:
            if tile.selected:
                tile.deselect()
                self.selected_tiles.remove(tile)
                print(f"I'm in Tiles deselect. Tile ID: {tile.id}")
                print(f"I'm in Tiles deselect. selected tiles after deselection: {tile.selected}")


class Tile:
    def __init__(self, index: int, x_offset: int, y_offset: int, draw: bool = True) -> None:
        self.params = Parameters()
        self.id = index
        self.x_offset: int = x_offset
        self.y_offset: int = y_offset
        self.width: int = self.params.tile_width
        self.height: int = self.params.tile_height
        self.color = RED  # use background color to have frame color seem transparent
        self.selected = False  # selection is a persistent state until deselection
        self.rules = Rules()  # rule set applies per tile

        if draw:
            self.get_face()
            self.overlay()
            self.get_outline()

    def get_face(self) -> None:
        """Get the tile face, i.e. a drawable area entity."""
        # load image and optimize with convert
        self.face = pygame.image.load(self.params.tiles_path.joinpath("Chun.png"))
        self.face = self.face.convert_alpha()
        self.face = pygame.transform.scale(self.face, (self.width, self.height))

    def overlay(self) -> None:
        """Get the tiles transparent overlay used for selection."""
        self.overlay = pygame.Surface(self.face.get_size(), pygame.SRCALPHA, 32)
        self.overlay = self.overlay.convert_alpha()
        self.overlay.fill((255, 255, 81, 120))

    def remove_overlay(self) -> None:
        """Remove the tiles transparent overlay."""
        self.overlay()
        # self.overlay = pygame.Surface(self.face.get_size(), pygame.SRCALPHA, 32)
        # self.overlay = self.overlay.convert_alpha()
        # self.overlay.fill((255, 255, 255, 255))

    def get_outline(self) -> None:
        """Get outline coordinates of the tile."""
        self.outline = self.face.get_rect()
        self.outline.topleft = (self.x_offset, self.y_offset)

    def check_clicked(self, event: pygame.event.Event) -> None:
        """Check if the mouse button was pressed.
        Select the tile if the position is within the tile bounding box and the tile has not been selected before.
        If the tile has been selected before, deselect it."""
        if not self.selected and self.outline.collidepoint(event.pos):
            self.selected = True
            print(self.id)
            return True  # return True because tile was clicked

        elif self.selected and self.outline.collidepoint(event.pos):
            # TODO: this also selects the screen
            print(self.id)
            self.deselect()
            return True  # return True because tile was clicked

    def deselect(self) -> None:
        self.selected = False
