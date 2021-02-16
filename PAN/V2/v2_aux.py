
import numpy as np
import MoNeT_MGDrivE as monet



def zeroDivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b!=0)

# #############################################################################
# Paths
# #############################################################################
def selectPath(USR):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/mgdrive2_paper/'
    else:
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/v2/Reviewers/'
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)



def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0], hLines=[0], wop=0, wopPrint=True):
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
        axTemp.axvline(vline, alpha=.5, zorder=10, lw=.075, color='#000000')

    if  wopPrint:
        axTemp.text(
            0.975, 0.2, int(wop),
            verticalalignment='bottom', horizontalalignment='right',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=15
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
