"""This script contains several classes handling specific tile positioning measures.
Notion is:
    | --> eastern and western border
    = --> top and bottom border
    x --> a tile
    - --> a gap between tiles
."""

from .parameters import Parameters

p = Parameters()


class NoneTouching:
    """TEST: Contains 2 pairs of tiles that do not touch.
    =====
    |x-x|
    |---|
    |x-x|
    =====
    """

    rows: int = 2
    cols: int = 2
    
    ul = (p.x_offset, p.y_offset)
    ur = (p.x_offset + p.tile_width + p.x_space, p.y_offset)
    lr = (p.x_offset + p.tile_width + p.x_space, p.y_offset + p.tile_height + p.y_space)
    ll = (p.y_offset, p.y_offset + p.tile_height + p.y_space)
    positions = [ul, ur, lr, ll]
    faces = ["hongzhong"] * len(positions)


class OneLevelTouching:
    """TEST: Contains touching tles on the same level.
    =====
    |xxxx|
    |xxxx|
    |xxxx|
    =====
    """

    rows: int = 3
    cols: int = 4
    positions: list = []

    for row in range(rows):
        for col in range(cols):
            positions.append((p.x_offset + col * (p.tile_width), p.y_offset + row * (p.tile_height)))
            
    faces = ["baiban", "nanfeng", "dongfeng", "beifeng", 
             "xifeng", "xifeng", "nanfeng", "beifeng", 
             "dongfeng", "qingfa", "qingfa", "baiban"]
