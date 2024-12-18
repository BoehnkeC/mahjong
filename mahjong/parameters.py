from pathlib import Path

from pydantic import BaseModel


class Parameters(BaseModel):
    tile_width: int = 50
    tile_height: int = int(tile_width * 1.5)
    num_pairs: int = 2
    num_tiles: int = num_pairs * 2
    x_offset: int = 50  # space between left/right edge and tile
    y_offset: int = 50  # space between top/bottom edge and tile
    x_space: int = 20  # space between tiles in x direction
    y_space: int = 20  # space between tiles in y direction
    rows: int = num_pairs  # number of rows
    cols: int = 2  # number of columns
    canvas_width: int = x_offset * 2 + tile_width * cols + x_space * (cols - 1)
    canvas_height: int = y_offset * 2 + tile_height * rows + y_space * (rows - 1)
    # tiles_path: Path = Path(__file__).parent.parent.joinpath("tiles")
    tiles_path: Path = Path("/Users/chris/Pictures")
