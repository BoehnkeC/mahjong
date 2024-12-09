import pygame

from .parameters import Parameters

GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Tiles:
    def __init__(self) -> None:
        self.tiles: list[Tile] | None = None

    def get_tiles(self, positions: list, draw: bool = True) -> None:
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

        if draw:
            self.get_face()
            self.get_outline()

    def get_face(self) -> None:
        self.face = pygame.image.load(self.params.tiles_path.joinpath("Front.png"))
        self.face.convert()  # optimize image format and make drawing faster
        self.face = pygame.transform.scale(self.face, (self.width, self.height))

    def get_outline(self) -> None:
        self.outline = self.face.get_rect()
        self.outline.topleft = (self.x_offset, self.y_offset)

    def check_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse button is pressed
            x, y = event.pos  # get x and y position of mouse click

            if self.outline.collidepoint(x, y):
                self.color = GREEN
