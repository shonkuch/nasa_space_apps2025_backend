from endpoint import get_image_at
from geo_coords_to_tile import geo_to_tile, MatrixCoords

for i in range(0, 9):
    coords: MatrixCoords = geo_to_tile(50.45466, 30.5238, i)
    img = get_image_at(coords, "2012-07-09")
