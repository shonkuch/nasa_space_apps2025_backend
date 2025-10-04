import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import folium
import urllib.request
import urllib.parse
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
from PIL import ImageDraw
import numpy as np
import pandas as pd
from owslib.wms import WebMapService
from IPython.display import Image, display
import geopandas as gpd
from shapely.geometry import box
import urllib.request
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.plot import show
import fiona
from datetime import datetime, timedelta
import asyncio


def download_image(layers: list[str]):
    print(f'Downloading {layers}')
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
    img = wms.getmap(layers=layers,  # Layers
        srs='epsg:4326',  # Map projection
        bbox=(-180, -90, 180, 90),  # Bounds
        size=(1200, 600),  # Image size
        time='2021-08-21',  # Time of data
        format='image/png',  # Image format
        transparent=True)  # Nodata transparency

    # Save output PNG to a file
    out = open(f'{layers[0]}_{datetime.now()}.png', 'wb')
    out.write(img.read())
    out.close()

def collect():
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

collect()