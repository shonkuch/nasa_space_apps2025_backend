import json
import xml.etree.ElementTree as xmlet
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import requests

def download_image(time, layers, size, matrix, col, row):
    print(f'Downloading {layers}')
    source = f"https://gibs-a.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?"
    params = f"\
TIME={time}\
&layer={",".join(layers)}\
&style=default\
&tilematrixset={size}\
&Service=WMTS&Request=GetTile\
&Version=1.0.0\
&Format=image%2Fjpeg\
&TileMatrix={matrix}\
&TileCol={col}\
&TileRow={row}"
    url = source + params
    response = requests.get(url)
    filename = f'{layers[0]}_{datetime.now()}.png'

    print(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print("Failed to download")


# def download_image(layers: list[str]):
#     wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
#     img = wms.getmap(layers=layers,  # Layers
#         srs='epsg:4326',  # Map projection
#         bbox=(-180, -90, 180, 90),  # Bounds
#         size=(1200, 600),  # Image size
#         time='2021-08-21',  # Time of data
#         format='image/png',  # Image format
#         transparent=True)  # Nodata transparency
#
#     # Save output PNG to a file
#     out = open(f'{layers[0]}_{datetime.now()}.png', 'wb')
#     out.write(img.read())
#     out.close()

def main():
    # Construct capability URL.
    wmsUrl = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetCapabilities'
    response = requests.get(wmsUrl)
    WmsTree = xmlet.fromstring(response.content)
    all_layers = []
    layerNumber = 0
    for child in WmsTree.iter():
        for layer in child.findall("./{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer//*/"):
            if layer.tag == '{http://www.opengis.net/wms}Layer':
                f = layer.find("{http://www.opengis.net/wms}Name")
                if f is not None:
                    all_layers.append(f.text)
                    layerNumber += 1
    all_layers = pd.Series(all_layers)
    all_layers = all_layers[all_layers.str.contains("MODIS_Terra")].sort_values()
    print(f'Layers: {len(all_layers)}')
    for layer in all_layers:
        download_image(
            datetime(2025, 10, 4, 0, 0, 0).strftime("%Y-%m-%dT%H:%M:%SZ"),
            [layer],
            # ['MODIS_Terra_CorrectedReflectance_TrueColor'],
            "250m", 6, 68, 25)

if __name__ == "__main__":
    main()