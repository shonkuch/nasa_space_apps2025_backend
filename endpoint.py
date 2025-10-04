import requests

def get_image_at():

    layer = "MODIS_Terra_CorrectedReflectance_TrueColor"
    style = "default"
    tile_matrix_set = "250m"
    tile_matrix = "7"
    tile_row = "26"
    tile_col = "94"
    time = "2012-07-09"
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

    if response.status_code == 200:
        with open("test.png", "wb") as f:
            f.write(response.content)
        print("Saved")
    else:
        print(f"Failed to fetch tile: HTTP {response.content}")

get_image_at()
