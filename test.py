from endpoint import get_full_tile
from geo_coords_to_tile import geo_to_tile, MatrixCoords, find_tile_neighbours
from matrix_settings import get_matrix_settings

#geo_coords = "64.0 -153.0" # Alaska
#geo_coords = "-51.8142779 -59.5318429" # Falkland islands
#geo_coords = "35.700330532 139.708997164" # Tokyo
#geo_coords = "30.054833114 31.223999104" # Cairo
geo_coords = "50.45466 30.5238" # Kyiv

lat = float(geo_coords.split(" ")[0])
lon = float(geo_coords.split(" ")[1])

#for i in range(0, 9):
#    coords: MatrixCoords = geo_to_tile(lat, lon, i)
#    img = get_image_at(coords, "2012-07-09")

# 250m geographic_with_clouds
# 1km vegetation
# 2km temp

matrix_type = "2km"

matrix_settings_dict = get_matrix_settings(matrix_type)
keys_list = list(matrix_settings_dict.keys())
keys_list.sort()

for i in range(1, keys_list[-1]):
    coords: [MatrixCoords] = find_tile_neighbours(geo_to_tile(lat, lon, i, matrix_type))
    img = get_full_tile(coords, "2012-07-09")
    print(f"Finished: {i}th at {matrix_type}")