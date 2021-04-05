
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt



def exportTracesPlotVideo(
    tS, nS, STYLE, PATH_IMG, append='', vLines=[0, 0]
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
    axTemp.axvspan(vLines[0], vLines[1], alpha=.5, facecolor='#ffffff', zorder=5)
    axTemp.axvline(vLines[0], alpha=0.25, ls='--', lw=1, color='#B1C0DD', zorder=10)

    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor='w', edgecolor='w',
            orientation='portrait', format='png',
            transparent=False, bbox_inches='tight', pad_inches=0.1
        )
    plt.close('all')
    return True