"""This script contains several classes handling specific tile positioning measures.
Notion is:
    | --> eastern and western border
    = --> top and bottom border
    x --> a tile
    - --> a gap between tiles
."""

from .parameters import Parameters


class NoneTouching:
    """TEST: Contains 2 pairs of tiles that do not touch.
    =====
    |x-x|
    |---|
    |x-x|
    =====
    """

    p = Parameters()
    positions = []
    for col in range(p.cols):
        for row in range(p.rows):
            positions.append(
                (
                    p.x_offset + (p.tile_width + p.x_space) * col,
                    p.y_offset + (p.tile_height + p.y_space) * row,
                )
            )
