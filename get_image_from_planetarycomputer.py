"""Script for searching the Microsoft Planetary Computer sentinel-2-l2a
collection. 
"""

__author__ = 'Daryl Suen'


import fiona
import pystac_client
import planetary_computer
import json
import pansharpen_functions as pf


########## Variables ##########################################################
catalog = "https://planetarycomputer.microsoft.com/api/stac/v1"
# Bounding box coordinates from QGIS Geometry Shapes plugin.
bbox_of_interest = [-119.991, 50.796, -119.221, 51.172]
# I happen to know it was clear this day and landsat 8 had a pass over the area.
time_of_interest = "2023-06-07"
collection = ['landsat-c2-l2']
cloud_cover = {"eo:cloud_cover": {"lt": 10}}
###############################################################################
items = pf.search(catalog, collection, bbox_of_interest, time_of_interest, cloud_cover)
pf. get_least_cloudy(items)

