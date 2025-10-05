from endpoint import get_full_tile
from geo_coords_to_tile import MatrixCoords, find_tile_neighbours, geo_to_tile


def make_master_call(lat, lon, matrix_type, matrix_level, time):
    coords: [MatrixCoords] = find_tile_neighbours(geo_to_tile(lat, lon, matrix_level, matrix_type))
    img = get_full_tile(coords, time)

    return img