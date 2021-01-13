

%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import osmnx as ox
ox.config(log_console=True)
ox.__version__

PTH = '/home/chipdelmal/Documents/WorkSims/PYF/GEO/'
point = (-17.0188, -149.5884)
(placeName, dist) = ('Onetahi', 1000)
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
fp = f'{PTH}/{placeName}.{extension}'
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
df.to_csv(f'{PTH}/{placeName}.csv', index=False)
###############################################################################
# Shapefile
###############################################################################
gdf_save = gdf.applymap(lambda x: str(x) if isinstance(x, list) else x)
gdf_save.drop(labels='nodes', axis=1).to_file(f'{PTH}/{placeName}.shp', driver='ESRI Shapefile')