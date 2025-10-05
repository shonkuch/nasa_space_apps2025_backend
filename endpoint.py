import io
import os

import requests
from PIL import Image

from crop_image_to_point import crop_image_to_point
from geo_coords_to_tile import MatrixCoords


### Get 3x3 square
def get_full_tile(matrix_coords_list: [MatrixCoords], time):
    images_generated = []

    for i in range(len(matrix_coords_list)):
        matrix_coords = matrix_coords_list[i]
        matrix_type = matrix_coords.matrix_type

        if matrix_type == "1km":
            layer = "MODIS_Terra_L3_NDVI_Monthly"
            output_format = "png"
        elif matrix_type == "2km":
            layer = "MODIS_Terra_L3_Land_Surface_Temp_Monthly_CMG_Day_TES"
            output_format = "png"
        else:
            layer = "MODIS_Terra_CorrectedReflectance_TrueColor"
            output_format = "jpg"

        style = "default"
        tile_matrix_set = matrix_type
        matrix_level = matrix_coords.matrix_level
        tile_row = matrix_coords.row
        tile_col = matrix_coords.col
        time = time

        tile_url = (
            f"https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/"
            f"{layer}/"
            f"{style}/"
            f"{time}/"
            f"{tile_matrix_set}/"
            f"{matrix_level}/"
            f"{tile_row}/"
            f"{tile_col}"
            f".{output_format}"
        )

        response = requests.get(tile_url)

        if response.status_code == 200:
            os.makedirs("results", exist_ok=True)

            img_bytes = io.BytesIO(response.content)
            img = Image.open(img_bytes)
            images_generated.append(img)

            print(f"Saved: {i+1}/{len(matrix_coords_list)}")
        else:
            raise ValueError("Cannot open this link")

    pixel_coords = matrix_coords_list[4]
    cols = 3
    rows = 3

    w, h = (512, 512)

    combined = Image.new("RGB", (cols * w, rows * h))

    for i, img in enumerate(images_generated):
        x = (i % cols) * w
        y = (i // cols) * h
        combined.paste(img, (x, y))

    # Save or show
    os.makedirs("results\\combined", exist_ok=True)
    os.makedirs("results\\cropped", exist_ok=True)
    #combined.save(f"results\\combined\\{pixel_coords.matrix_level}_combined.jpg")
    cropped = crop_image_to_point(combined, pixel_coords)
    #cropped.save(f"results\\cropped\\{pixel_coords.matrix_level}_cropped.jpg")
    return cropped
