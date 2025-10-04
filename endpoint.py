import requests
from PIL import Image

def stitch():
    images = [Image.open(path) for path in [
        "2_0_0.jpg",
        "2_0_1.jpg",
        "2_1_0.jpg",
        "2_1_1.jpg"
    ]]
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

if __name__ == "__main__":
    # Starting image
    get_image_at("250m", 1, 0, 0, "2012-07-09")

    # Combining sub-images into one image
    for i in range(2):
        for j in range(2):
            get_image_at("250m", 2, i, j, "2012-07-09")
    stitch()

    # 1_0_0.jpg (512x512) and patched.jpg (1024x1024) should look the same

