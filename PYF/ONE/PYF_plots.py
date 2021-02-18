
import math
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# from mpl_toolkits.basemap import Basemap


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


COLORS = [
        rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        rescaleRGBA((255, 0, 152, 255/1.75)),    # 1: Magenta
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
                lw=3.5 * math.log(1 + lw * mtxTransitions[j][i]),
                alpha=min(.5, .5 * math.log(1 + la * mtxTransitions[j][i])),
                solid_capstyle='round', c=c,
                zorder=-5
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


# #############################################################################
# Videos
# #############################################################################
def plotMapSHP(
        filename, fig, ax, pts, BLAT, BLNG, 
        drawCoasts=True, ptColor='#66ff00'
):
    # Hi-Res Basemap ----------------------------------------------------------
    mH = Basemap(
        projection='merc', lat_ts=20, resolution='h', ax=ax,
        llcrnrlat=BLAT[0], urcrnrlat=BLAT[1], 
        llcrnrlon=BLNG[0], urcrnrlon=BLNG[1]   
    )
    mH.readshapefile(
        filename, 'PYF', 
        drawbounds=True, linewidth=15, color=COLORS[4], zorder=-2
    )
    mH.readshapefile(
        filename, 'PYF', 
        drawbounds=True, linewidth=4, color=COLORS[0], zorder=-1
    )
    mH.readshapefile(
        filename, 'PYF', 
        drawbounds=True, linewidth=1, color=COLORS[3], zorder=0
    )
    # Lo-Res Basemap ----------------------------------------------------------
    mH.scatter(
        list(pts['lons']), list(pts['lats']), latlon=True,
        alpha=.1, marker='.', 
        s=popsToPtSize(list(pts['pops']), offset=10, amplitude=50),
        color=ptColor, zorder=3
    )
    # Ax parameters -----------------------------------------------------------
    ax.tick_params(
        axis='both', which='both',
        bottom=True, top=False, left=True, right=False,
        labelbottom=True, labelleft=True
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # Return values -----------------------------------------------------------
    return (fig, ax, mH)


def floatToHex(a, minVal=0, maxVal=1):
    intVal = int(np.interp(a, (minVal, maxVal), (0, 255)))
    return intVal


def popsToPtSize(pops, offset=10, amplitude=10):
    # return [max(offset, amplitude * math.log(i, 1.1)) for i in pops]
    return [max(offset, amplitude * (i**(1/2.5))) for i in pops]


def plotPopsOnMap(
    fig, ax, mapR, 
    lngs, lats, fractions, pops, 
    color='#ed174b', marker=(6, 0), edgecolor='#ffffff', lw=10,
    offset=10, amplitude=10, alpha=.85
):
    # print(fractions)
    colors = [color + '%02x' % floatToHex(i*alpha) for i in fractions]
    ptSize = popsToPtSize(pops, offset=offset, amplitude=amplitude)
    mapR.scatter(
        lngs, lats, 
        latlon=True, marker=marker,
        s=popsToPtSize(pops, offset=offset, amplitude=amplitude),
        c=colors, ax=ax, edgecolors=edgecolor, lw=lw
    )
    return (fig, ax, mapR)


def plotGenePopsOnMap(
    fig, ax, mapR,
    lngs, lats, colors, 
    GC_FRA, time, edgecolor='#ffffff',
    marker=(6, 0), offset=10, amplitude=10, alpha=.85, lw=2
):
    geneFraSlice = np.asarray([i[time] for i in GC_FRA]).T
    for gIx in range(geneFraSlice.shape[0]-1):
        (fig, ax, mapR) = plotPopsOnMap(
            fig, ax, mapR, 
            lngs, lats, geneFraSlice[gIx], geneFraSlice[-1],
            color=colors[gIx], marker=marker,
            offset=offset, amplitude=amplitude,
            alpha=alpha, edgecolor=edgecolor, lw=lw
        )
    return (fig, ax, mapR)



def plotMapFrame(
    filenameSHP,
    time, UA_sites, BLAT, BLNG, DRV_COL, GC_FRA, lngs, lats, EXP_VID,
    offset=2.5, amplitude=2, alpha=.35, marker=(6, 0), DPI=250, 
    edgecolor='#ffffff', lw=2
):
    print('* Exporting {}'.format(str(time).zfill(4)), end='\r')
    # Create map --------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 10))
    (fig, ax, mapR) = plotMapSHP(
        filenameSHP, fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff'
    )
    # Pops --------------------------------------------------------------------
    (fig, ax, mapR) = plotGenePopsOnMap(
        fig, ax, mapR,
        lngs, lats, DRV_COL, 
        GC_FRA, time, edgecolor=edgecolor,
        marker=marker, offset=offset, amplitude=amplitude, alpha=alpha, lw=lw
    )
    ax.text(
        0.75, 0.1, str(time).zfill(4), 
        horizontalalignment='center', verticalalignment='center', 
        transform=ax.transAxes, fontsize=30
    )
    quickSaveFig(
        '{}/{}.png'.format(EXP_VID, str(time).zfill(4)),
        fig, dpi=DPI
    )
    plt.close(fig)