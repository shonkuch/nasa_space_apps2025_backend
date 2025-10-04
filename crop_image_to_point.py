from PIL import Image, ImageDraw

from geo_coords_to_tile import MatrixCoords


def crop_image_to_point(tile_img_path: str, matrix_coords: MatrixCoords):
    img = Image.open(tile_img_path)
    draw = ImageDraw.Draw(img)
    tile_width, tile_height = img.size

    pixel_x = matrix_coords.pixel_x
    pixel_y = matrix_coords.pixel_y
    print(f"At {pixel_x}.{pixel_y}")

    crop_size = 256
    # Full crop size = 2 * crop_size
    left = max(pixel_x - crop_size, 0)
    upper = max(pixel_y - crop_size, 0)
    right = min(pixel_x + crop_size, tile_width)
    lower = min(pixel_y + crop_size, tile_height)

    #img = img.crop((left, upper, right, lower))
    draw.rectangle([left, upper, right, lower], outline="red", width=5)

    return img
