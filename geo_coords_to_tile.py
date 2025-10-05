import math

from matrix_settings import get_matrix_settings


def geo_to_tile(lat, lon, matrix_level, matrix_type, top_left=(-180.0, 90.0)):
    lon0, lat0 = top_left

    settings = get_matrix_settings(matrix_type)

    tile_width_px = settings[matrix_level]['TileWidth']
    tile_height_px = settings[matrix_level]['TileHeight']

    matrix_width = settings[matrix_level]['MatrixWidth']
    matrix_height = settings[matrix_level]['MatrixHeight']

    # Degrees per tile
    tile_deg_x = 360.0 / matrix_width
    tile_deg_y = 180.0 / matrix_height

    # Tile indices
    tile_col = math.floor((lon - lon0) / tile_deg_x)
    tile_row = math.floor((lat0 - lat) / tile_deg_y)

    # To prevent bad negatives
    tile_col = max(0, min(tile_col, matrix_width - 1))
    tile_row = max(0, min(tile_row, matrix_height - 1))

    # Pixel offset inside tile
    pixel_x = ((lon - lon0) % tile_deg_x) / tile_deg_x * tile_width_px
    pixel_y = ((lat0 - lat) % tile_deg_y) / tile_deg_y * tile_height_px

    return MatrixCoords(matrix_level, matrix_type, tile_col, tile_row, pixel_x, pixel_y)

class MatrixCoords:
    def __init__(self, matrix_level, matrix_type, col, row, pixel_x, pixel_y):
        self.matrix_level = matrix_level
        self.matrix_type = matrix_type
        self.col = col
        self.row = row
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

    matrix_level: int
    col: float
    row: float
    pixel_x: float
    pixel_y: float
    matrix_type: str

    def __str__(self):
        return f"Tile of level {self.matrix_level}: {self.col} col, {self.row} row"

def find_tile_neighbours(matrix_coords:MatrixCoords):
    l = matrix_coords.matrix_level
    c = matrix_coords.col
    r = matrix_coords.row
    pixel_x = matrix_coords.pixel_x
    pixel_y = matrix_coords.pixel_y

    matrix_type = matrix_coords.matrix_type
    settings = get_matrix_settings(matrix_type)

    mw = settings[l]['MatrixWidth']
    mh = settings[l]['MatrixHeight']
    neighbours = [
        MatrixCoords(l, matrix_type, (mw + c - 1) % mw, (mh + r - 1) % mh, 0, 0), # Top-left
        MatrixCoords(l, matrix_type, c, (mh + r - 1) % mh, 0, 0), # Top
        MatrixCoords(l, matrix_type, (mw + c + 1) % mw, (mh + r - 1) % mh, 0, 0), # Top-right
        MatrixCoords(l, matrix_type, (mw + c - 1) % mw, r, 0, 0), # Left
        MatrixCoords(l, matrix_type, c, r, pixel_x + 512, pixel_y + 512),  # Original, pixel_x & pixel_y shifted by 512
        MatrixCoords(l, matrix_type, (mw + c + 1) % mw, r, 0, 0), # Right
        MatrixCoords(l, matrix_type, (mw + c - 1) % mw, (mh + r + 1) % mh, 0, 0), # Bottom-left
        MatrixCoords(l, matrix_type, c, (mh + r + 1) % mh, 0, 0), # Bottom
        MatrixCoords(l, matrix_type, (mw + c + 1) % mw, (mh + r + 1) % mh, 0, 0) # Bottom-right
    ]
    return neighbours