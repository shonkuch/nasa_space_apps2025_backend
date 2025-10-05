from endpoint import get_full_tile
from geo_coords_to_tile import geo_to_tile, MatrixCoords, find_tile_neighbours
from matrix_settings import get_matrix_settings
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from API!"}

@app.get("/api/echo/{text}")
def echo_text(text: str):
    geo_coords = "50.45466 30.5238"  # Kyiv

    lat = float(geo_coords.split(" ")[0])
    lon = float(geo_coords.split(" ")[1])

    # 250m geographic_with_clouds
    # 1km vegetation
    # 2km temp

    matrix_type = "2km"

    matrix_settings_dict = get_matrix_settings(matrix_type)
    keys_list = list(matrix_settings_dict.keys())
    keys_list.sort()

    coords: [MatrixCoords] = find_tile_neighbours(geo_to_tile(lat, lon, 3, matrix_type))
    img = get_full_tile(coords, "2012-07-09")

    return {"img": img}