import os

import requests
from PIL import Image

from crop_image_to_point import crop_image_to_point
from geo_coords_to_tile import MatrixCoords


def get_image_at(matrix_coords: MatrixCoords, time):

    # layer = "MODIS_Terra_CorrectedReflectance_TrueColor"
    # style = "default"
    # tile_matrix_set = "250m"
    # tile_matrix = "7"
    # tile_row = "27"
    # tile_col = "94"
    # time = "2012-07-09"
    # output_format = "jpg"

    layer = "MODIS_Terra_CorrectedReflectance_TrueColor"
    style = "default"
    tile_matrix_set = "250m"
    matrix_level = matrix_coords.matrix_level
    tile_row = matrix_coords.row
    tile_col = matrix_coords.col
    time = time
    output_format = "jpg"

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

    # https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?REQUEST=GetCapabilities
    # ^ - for checking available formats

    print(f"Starting at: {matrix_level}: {matrix_coords.row} row, {matrix_coords.col} col")
    response = requests.get(tile_url)
    print(tile_url)

    if response.status_code == 200:
        os.makedirs("results", exist_ok=True)

        img_path = f"results\\{matrix_level}.jpg"

        with open(img_path, "wb") as f:
            f.write(response.content)

            crop_image_to_point(img_path, matrix_coords).save(img_path)

        print("Saved")
    else:
        print(f"Failed to fetch tile: HTTP {response.content}")

### Get 3x3 square
def get_full_tile(matrix_coords_list: [MatrixCoords], time):
    paths = []

    for i in range(len(matrix_coords_list)):
        matrix_coords = matrix_coords_list[i]
        layer = "MODIS_Terra_CorrectedReflectance_TrueColor"
        style = "default"
        tile_matrix_set = "250m"
        matrix_level = matrix_coords.matrix_level
        tile_row = matrix_coords.row
        tile_col = matrix_coords.col
        time = time
        output_format = "jpg"

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

        # https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?REQUEST=GetCapabilities
        # ^ - for checking available formats

        print(f"Starting at: {matrix_level}: {matrix_coords.row} row, {matrix_coords.col} col")
        response = requests.get(tile_url)
        print(tile_url)

        if response.status_code == 200:
            os.makedirs("results", exist_ok=True)

            img_path = f"results\\{matrix_level}_{i}.jpg"

            with open(img_path, "wb") as f:
                f.write(response.content)
                paths.append(img_path)
                #crop_image_to_point(img_path, matrix_coords).save(img_path)

            print("Saved")
        else:
            paths.append(None)
            print(f"Failed to fetch tile: HTTP {response.content}")

    pixel_coords = matrix_coords_list[4] # original image
    images = [Image.open(path) for path in paths]
    cols = 3
    rows = 3

    w, h = (512, 512)

    combined = Image.new("RGB", (cols * w, rows * h))

    for i, img in enumerate(images):
        x = (i % cols) * w
        y = (i // cols) * h
        combined.paste(img, (x, y))

    # Save or show
    combined.save(f"results\\{pixel_coords.matrix_level}_combined.jpg")
    crop_image_to_point(f"results\\{pixel_coords.matrix_level}_combined.jpg", pixel_coords).save(f"results\\{pixel_coords.matrix_level}_cropped.jpg")


# def recreate_parent(matrix, row, col):
#     get_image_at(matrix, row, col, "2012-07-09")
#     names = []
#     for i in range(2):
#         for j in range(2):
#             names.append(f"{matrix+1}_{i+(2*row)}_{j+(2*col)}.jpg")
#             get_image_at(matrix+1, i+(2*row), j+(2*col), "2012-07-09")
#
#     images = [Image.open(path) for path in names]
#     cols = 2
#     rows = 2
#
#     w, h = (512, 512)
#
#     combined = Image.new("RGB", (cols * w, rows * h))
#
#     for i, img in enumerate(images):
#         x = (i % cols) * w
#         y = (i // cols) * h
#         combined.paste(img, (x, y))
#
#     # Save or show
#     combined.save("patched.jpg")


#if __name__ == "__main__":
    # Calculates coordinates for children and joins them to resemble original image
    #recreate_parent(3, 0, 4)
