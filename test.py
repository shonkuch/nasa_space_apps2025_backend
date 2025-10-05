from endpoint import get_image_at, get_full_tile
from geo_coords_to_tile import geo_to_tile, MatrixCoords, find_tile_neighbours

#geo_coords = "64.0 -153.0" # Alaska
#geo_coords = "-51.8142779 -59.5318429" # Falkland islands
#geo_coords = "35.700330532 139.708997164" # Tokyo
#geo_coords = "30.054833114 31.223999104" # Cairo
geo_coords = "50.45466 30.5238" # Kyiv

lat = float(geo_coords.split(" ")[0])
lon = float(geo_coords.split(" ")[1])

# for i in range(0, 9):
#     coords: MatrixCoords = geo_to_tile(lat, lon, i)
#     img = get_image_at(coords, "2012-07-09")

# for i in range(0, 9):
coords: [MatrixCoords] = find_tile_neighbours(geo_to_tile(lat, lon, 8))
img = get_full_tile(coords, "2012-07-09")