

%matplotlib inline
import pandas as pd
import osmnx as ox
import matplotlib.pyplot as plt
ox.config(log_console=True)
ox.__version__


point = (-17.0188, -149.5884)
dist = 1000
placeName = 'Onetahi'
###############################################################################
# Image config
###############################################################################
(img_folder, extension, size) = ('images', 'png', 240)
tags = {'building': True}
###############################################################################
# Get footprints
###############################################################################
gdf = ox.geometries_from_point(point, tags, dist=dist)
gdf_proj = ox.project_gdf(gdf)
fp = f'./{img_folder}/{placeName}.{extension}'
fig, ax = ox.plot_footprints(
    gdf_proj, filepath=fp, 
    dpi=400, save=True, show=False, close=True
)
###############################################################################
# Centroids
###############################################################################
bounds = list(gdf['geometry'])
centroids = [[list(i)[0] for i in j.centroid.xy] for j in bounds]
(lons, lats) = list(zip(*centroids))
df = pd.DataFrame({'lons': lons, 'lats': lats})
df.to_csv(f'./data/{placeName}.csv', index=False)