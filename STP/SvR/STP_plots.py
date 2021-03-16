
import math
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import STP_dataAnalysis as da
import STP_functions as fun
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


COLORS = [
        rescaleRGBA((47, 28, 191, 255/2.5)),    # 0: Faded navy blue
        rescaleRGBA((255, 0, 152, 255/1)),      # 1: Magenta
        rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        rescaleRGBA((255, 255, 255, 255/1)),    # 3: White
        rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        rescaleRGBA((0, 0, 0, 255/5))           # 5: Black
    ]


def exportTracesPlot(
    tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0], hLines=[0], 
    wop=0, wopPrint=True, cpt=0, cptPrint=False, poe=0, poePrint=False
):
    figArr = monet.plotNodeTraces(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.axes.xaxis.set_visible(False)
    axTemp.axes.yaxis.set_visible(False)
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.set_axis_off()
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    days = tS['landscapes'][0].shape[0]
    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] < vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#3687ff', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-.', lw=.35, color='#3687ff', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-.', lw=.35, color='#3687ff', zorder=0)

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] > vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#FF5277', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-.', lw=.35, color='#FF1A4B', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-.', lw=.35, color='#FF1A4B', zorder=0)

    axTemp.axhline(
            hLines, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000'
        )
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000')

    if  wopPrint:
        axTemp.text(
            0.7, 0.05, 'WOP: '+str(int(wop)),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=12.5
        )
    if cptPrint:
        axTemp.text(
            0.7, 0.1, 'CPT: {:.3f}'.format(cpt),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=12.5
        )     
    
    if poePrint:
        axTemp.text(
            0.7, 0.15, 'POE: {:.3f}'.format(poe),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=12.5
        )        

    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=0
        )
    plt.close('all')
    return True


# #############################################################################
# Videos
# #############################################################################
def plotMap(
        fig, ax, pts, BLAT, BLNG, 
        drawCoasts=True, ptColor='#66ff00'
):
    # Hi-Res Basemap ----------------------------------------------------------
    mH = Basemap(
        projection='merc', ax=ax, lat_ts=20, resolution='h',
        llcrnrlat=BLAT[0], urcrnrlat=BLAT[1],
        llcrnrlon=BLNG[0], urcrnrlon=BLNG[1],
    )
    mL = Basemap(
        projection='merc', ax=ax, lat_ts=20, resolution='i',
        llcrnrlat=BLAT[0], urcrnrlat=BLAT[1],
        llcrnrlon=BLNG[0], urcrnrlon=BLNG[1],
    )
    if drawCoasts:
        mH.drawcoastlines(color=COLORS[0], linewidth=5, zorder=-2)
        mH.drawcoastlines(color=COLORS[3], linewidth=.5, zorder=-1)
        mL.drawcoastlines(color=COLORS[4], linewidth=15, zorder=-3)
    # Lo-Res Basemap ----------------------------------------------------------
    mH.scatter(
        list(pts['lon']), list(pts['lat']), latlon=True,
        alpha=.05, marker='.', 
        s=popsToPtSize(list(pts['pop']), offset=10, amplitude=10),
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
    return (fig, ax, mL)


def floatToHex(a, minVal=0, maxVal=1):
    intVal = int(np.interp(a, (minVal, maxVal), (0, 255)))
    return intVal


def popsToPtSize(pops, offset=10, amplitude=10):
    # return [max(offset, amplitude * math.log(i, 1.1)) for i in pops]
    return [max(offset, amplitude * (i**(1/2.5))) for i in pops]


def plotPopsOnMap(
    fig, ax, mapR, 
    lngs, lats, fractions, pops, 
    color='#ed174b', marker=(6, 0), edgecolor='#ffffff',
    offset=10, amplitude=10, alpha=.85
):
    # print(fractions)
    colors = [color + '%02x' % floatToHex(i*alpha) for i in fractions]
    mapR.scatter(
        lngs, lats, 
        latlon=True, marker=marker,
        s=popsToPtSize(pops, offset=offset, amplitude=amplitude),
        c=colors, ax=ax, edgecolors=edgecolor
    )
    return (fig, ax, mapR)


def plotGenePopsOnMap(
    fig, ax, mapR,
    lngs, lats, colors, 
    GC_FRA, time, edgecolor='#ffffff',
    marker=(6, 0), offset=10, amplitude=10, alpha=.85
):
    geneFraSlice = np.asarray([i[time] for i in GC_FRA]).T
    for gIx in range(geneFraSlice.shape[0]-1):
        (fig, ax, mapR) = plotPopsOnMap(
            fig, ax, mapR, 
            lngs, lats, geneFraSlice[gIx], geneFraSlice[-1],
            color=colors[gIx], marker=marker,
            offset=offset, amplitude=amplitude,
            alpha=alpha, edgecolor=edgecolor
        )
    return (fig, ax, mapR)



def plotMapFrame(
    time, UA_sites, BLAT, BLNG, DRV_COL, GC_FRA, lngs, lats, EXP_VID,
    offset=2.5, amplitude=2, alpha=.35, marker=(6, 0), DPI=250, 
    edgecolor='#ffffff'
):
    print('* Exporting {}'.format(str(time).zfill(4)), end='\r')
    # Create map --------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 10))
    (fig, ax, mapR) = plotMap(
        fig, ax, UA_sites, BLAT, BLNG, ptColor='#6347ff'
    )
    # Pops --------------------------------------------------------------------
    (fig, ax, mapR) = plotGenePopsOnMap(
        fig, ax, mapR,
        lngs, lats, DRV_COL, 
        GC_FRA, time, edgecolor=edgecolor,
        marker=marker, offset=offset, amplitude=amplitude, alpha=alpha
    )
    ax.text(
        0.75, 0.1, str(time).zfill(4), 
        horizontalalignment='center', verticalalignment='center', 
        transform=ax.transAxes, fontsize=30
    )
    fun.quickSaveFig(
        '{}/{}.png'.format(EXP_VID, str(time).zfill(4)),
        fig, dpi=DPI
    )
    plt.close(fig)

# #############################################################################
# Networks
# #############################################################################

def plotMatrix(psi):
    (fig, ax) = plt.subplots(figsize=(8, 8))
    ax.set_aspect(1)
    ax.set_axis_off()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.imshow(psi, cmap='Purples')
    return (fig, ax)

def plotNetwork(fig, ax, mtxTransitions, ptsB, ptsA, c='#dd5fb', lw=.4, la=5):
    (aNum, bNum) = (ptsA.shape[0], ptsB.shape[0])
    for j in range(aNum):
        src = ptsA[j]
        for i in range(bNum):
            snk = ptsB[i]
            plt.plot(
                [src[0], snk[0]], [src[1], snk[1]],
                lw=math.log(1 + lw * mtxTransitions[j][i]),
                alpha=min(1, math.log(1 + la * mtxTransitions[j][i])),
                solid_capstyle='round', c=c,
                zorder=0
            )
    return (fig, ax)


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
