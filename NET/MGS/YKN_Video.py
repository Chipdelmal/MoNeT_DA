#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
import time
import numpy as np
import pandas as pd
from os import path
from sys import argv
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image
import MGSurvE as srv
matplotlib.use('agg')
# https://github.com/matplotlib/matplotlib/issues/20067


if srv.isNotebook():
    (LND_TYPE, ID) = ('YKN', '10')
else:
    (LND_TYPE, ID) = (argv[1], argv[2])
# Constants -------------------------------------------------------------------
OUT_PTH = '/RAID5/marshallShare/MGSurvE_Yorkeys'
fPat = '{}_{}_'.format(LND_TYPE, ID)
IMG_PTH = path.join(OUT_PTH, fPat+'VID')
srv.makeFolder(IMG_PTH)
DPI = 200
###############################################################################
# Load Landscape
############################################################################### 
lnd = srv.loadLandscape(OUT_PTH, fPat+'TRP', fExt='pkl')
dat = srv.importLog(OUT_PTH, fPat+'LOG')
TCOL = {
    0: '#f7258515', 1: '#fe5f5515', 2: '#5ddeb125', 
    3: '#f038ff15', 4: '#e2ef7015', 5: '#9381ff15', 
}
###############################################################################
# Kernel Plot
############################################################################### 
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
(fig, ax) = srv.plotTrapsKernels(
    fig, ax, lnd, 
    distRange=(0, 125), colors=TCOL, aspect=.1
)
fig.savefig(
    path.join(OUT_PTH, '{}{}_{}_KER.png'.format(OUT_PTH, LND_TYPE, ID)), 
    facecolor='w', bbox_inches='tight', pad_inches=0.1, dpi=300
)
plt.close('all')
###############################################################################
# Plot Loop
############################################################################### 
(gaMin, gaTraps, gens) = (dat['min'], dat['traps'], dat.shape[0])
bbox = lnd.getBoundingBox()
i=10
for i in range(0, len(gaMin)):
    print("* Exporting frame {:05d}".format(i), end='\r')
    ###########################################################################
    # Reshape and update traps
    ###########################################################################
    trapsCoords = np.reshape(
        np.fromstring(gaTraps[i][1:-1], sep=','), (-1, 2)
    ).T
    trapsLocs = pd.DataFrame(
        np.vstack([trapsCoords, lnd.trapsTypes, lnd.trapsFixed]).T, 
        columns=['lon', 'lat', 't', 'f']
    )
    trapsLocs['t']=trapsLocs['t'].astype('int64')
    trapsLocs['f']=trapsLocs['f'].astype('int64')
    lnd.updateTraps(trapsLocs, lnd.trapsKernels)
    ###########################################################################
    # Plot Figure
    ###########################################################################
    (fig, ax) = (
        plt.figure(figsize=(15, 15)),
        plt.axes(projection=ccrs.PlateCarree())
    )
    (fig, ax) = lnd.plotTraps(fig, ax, colors=TCOL)
    (fig, ax) = srv.plotClean(fig, ax, bbox=lnd.landLimits)
    ax.text(
        0.75, 0.15, '{:.4f}'.format(gaMin[i]),
        horizontalalignment='center', verticalalignment='center',
        fontsize=50, color='#00000011',
        transform=ax.transAxes, zorder=5
    )
    ax.text(
        0.75, 0.10, 'gens: {:04d}'.format(i),
        horizontalalignment='center', verticalalignment='center',
        fontsize=25, color='#00000011',
        transform=ax.transAxes, zorder=5
    )
    pthSave = path.join(IMG_PTH, '{}{:05d}.png'.format(fPat, i))
    fig.savefig(
        pthSave, 
        dpi=DPI, bbox_inches='tight', 
        pad_inches=0.1, transparent=True
    )
    srv.plotsClearMemory()
    fig.clf()
    plt.close()
    plt.close("all")
    gc.collect()
    ###########################################################################
    # Overlay Brute-force
    ###########################################################################
    time.sleep(.75)
    background = Image.open(path.join(OUT_PTH, LND_TYPE+'_CLN.png')).convert('RGBA')
    foreground = Image.open(pthSave).convert('RGBA')
    (w, h) = background.size
    background = background.crop((0, 0, w, h))
    foreground = foreground.resize((int(w/1), int(h/1)), Image.ANTIALIAS)
    background.paste(foreground, (0, 0), foreground)
    background.save(pthSave, dpi=(DPI, DPI))
    background.close()
    foreground.close()
###############################################################################
# Compile Video
############################################################################### 
subprocess.run([
    "ffmpeg", "-y",
    "-start_number", "0",
    "-r", "4",
    "-f", "image2",
    "-i", path.join(IMG_PTH, fPat+"%05d.png"),
    "-s", "1920x1080", 
    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", 
    "-vcodec", "libx264", 
    "-preset", "veryslow", 
    "-crf", "15",
    "-pix_fmt", "yuv420p",
    path.join(OUT_PTH, fPat+"MOV.mp4")
])



 