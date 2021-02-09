
import math
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# from mpl_toolkits.basemap import Basemap


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


COLORS = [
        rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        rescaleRGBA((255, 0, 152, 255/2.5)),    # 1: Magenta
        rescaleRGBA((37, 216, 17, 255/8)),      # 2: Bright green
        rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]

# #############################################################################
# Network
# #############################################################################
def plotNetworkOnMap(map, mtxTransitions, ptsB, ptsA, c='#dd5fb', lw=.4, la=5):
    (aNum, bNum) = (ptsA.shape[0], ptsB.shape[0])
    for j in range(aNum):
        src = ptsA[j]
        for i in range(bNum):
            snk = ptsB[i]
            map.plot(
                [src[0], snk[0]], [src[1], snk[1]], latlon=True,
                lw=math.log(1 + lw * mtxTransitions[j][i]),
                alpha=min(1, math.log(1 + la * mtxTransitions[j][i])),
                solid_capstyle='round', c=c,
                zorder=0
            )
    return map


# #############################################################################
# Save
# #############################################################################
def quickSaveFig(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, bbox_inches='tight', pad_inches=.02
     )