import folium
import os
import numpy as np

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import geopandas as gpd
import geopandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import MultiPolygon, Polygon
import rasterio as rio
from rasterio.plot import show
import rasterio.mask
import fiona
from zipfile import ZipFile

def get_NDVI():
    user = 'serafimyaronskii'
    password = 'edxrfcvgt'

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

    nReserve = gpd.read_file('data.json')

    footprint = None
    for i in nReserve['geometry']:
        footprint = i

    products = api.query(footprint,
                         date = ('20190601', '20190626'),
                         platformname = 'Sentinel-2',
                         processinglevel = 'Level-2A',
                         cloudcoverpercentage = (0,1000))

    products_gdf = api.to_geodataframe(products)
    products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

    a = products_gdf_sorted.title.keys()[0]
    b = products_gdf_sorted.title.values[0]


    api.download(str(products_gdf_sorted.title.keys()[0]))

    with ZipFile(str(b)+'.zip', 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall()

    R10 = str(b) + '.SAFE/GRANULE/'
    R10 = str(b) + '.SAFE/GRANULE/'+ os.listdir(R10)[0] +'/IMG_DATA/R10m/'
    for i in os.listdir(R10):
      if 'B04' in i:
        b4 = rio.open(R10+i)
      if 'B03' in i:
        b3 = rio.open(R10+i)
      if 'B02' in i:
        b2 = rio.open(R10+i)

    #b4.count, b4.width, b4.height

    with rio.open('RGB.tiff','w',driver='Gtiff', width=b4.width, height=b4.height,
                  count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b2.read(1),1)
        rgb.write(b3.read(1),2)
        rgb.write(b4.read(1),3)
        rgb.close()


    nReserve_proj = nReserve.to_crs({'init': 'epsg:32633'})

    with rio.open("RGB.tiff") as src:
        out_image, out_transform = rio.mask.mask(src, nReserve_proj.geometry, crop=False)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

    with rasterio.open("RGB_masked.tif", "w", **out_meta) as dest:
        dest.write(out_image)

    R10 = str(b) + '.SAFE/GRANULE/'
    R10 = str(b) + '.SAFE/GRANULE/'+ os.listdir(R10)[0] +'/IMG_DATA/R10m/'
    for i in os.listdir(R10):
      if 'B04' in i:
        b4 = rio.open(R10+i)
      if 'B08' in i:
        b8 = rio.open(R10+i)

    red = b4.read()
    nir = b8.read()

    ndvi = (nir.astype(float)-red.astype(float))/(nir+red)

    meta = b4.meta

    meta.update(driver='GTiff')
    meta.update(dtype=rasterio.float32)

    with rasterio.open('NDVI.tif', 'w', **meta) as dst:
        dst.write(ndvi.astype(rasterio.float32))

    msk = rio.open(r"NDVI.tif")
    fig, ax = plt.subplots(1, figsize=(18, 18))
    show(msk.read())
    fig.savefig('saved_figure.png')

