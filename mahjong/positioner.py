"""This script contains several classes handling specific tile positioning measures.
Notion is:
    | --> eastern and western border
    = --> top and bottom border
    x --> a tile
    - --> a gap between tiles
."""


class NoneTouching:
    """TEST: Contains 2 pairs of tiles that do not touch.
    =====
    |x-x|
    |---|
    |x-x|
    =====
    """

    ul = (50, 50)
    ur = (120, 50)
    lr = (120, 145)
    ll = (50, 145)
    positions = [ul, ur, lr, ll]
