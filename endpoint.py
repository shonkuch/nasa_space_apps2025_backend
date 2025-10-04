import requests
from PIL import Image

def get_image_at(scale, matrix, row, col, time):

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
    tile_matrix_set = scale
    tile_matrix = matrix
    tile_row = row
    tile_col = col
    time = time
    output_format = "jpg"

    tile_url = (
        f"https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/"
        f"{layer}/"
        f"{style}/"
        f"{time}/"
        f"{tile_matrix_set}/"
        f"{tile_matrix}/"
        f"{tile_row}/"
        f"{tile_col}"
        f".{output_format}"
    )

    # https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?REQUEST=GetCapabilities
    # ^ - for checking available formats

    response = requests.get(tile_url)
    print(tile_url)

    if response.status_code == 200:
        with open(f"{matrix}_{row}_{col}.jpg", "wb") as f:
            f.write(response.content)
        print("Saved")
    else:
        print(f"Failed to fetch tile: HTTP {response.content}")

def recreate_parent(matrix, row, col):
    get_image_at("250m", matrix, row, col, "2012-07-09")
    names = []
    for i in range(2):
        for j in range(2):
            names.append(f"{matrix+1}_{i+(2*row)}_{j+(2*col)}.jpg")
            get_image_at("250m", matrix+1, i+(2*row), j+(2*col), "2012-07-09")

    images = [Image.open(path) for path in names]
    cols = 2
    rows = 2

    w, h = (512, 512)

    combined = Image.new("RGB", (cols * w, rows * h))

    for i, img in enumerate(images):
        x = (i % cols) * w
        y = (i // cols) * h
        combined.paste(img, (x, y))

    # Save or show
    combined.save("patched.jpg")


if __name__ == "__main__":
    # Calculates coordinates for children and joins them to resemble original image
    recreate_parent(3, 0, 4)

