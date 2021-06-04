

from os import path
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt

###############################################################################
# Save Figure
###############################################################################
def quickSaveFig(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, bbox_inches='tight', pad_inches=.02
     )


def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1,
            transparent=False
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        vLines=vLines, transparent=transparent
    )
    return None



def exportPreTracesPlotWrapper(
        expIx, fLists, STYLE, PT_IMG,
        border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
        xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1,
        transparent=False
    ):
    ter.printProgress(expIx+1, xpNum, digs)
    (_, repDta) = [pkl.load(file) for file in (fLists[expIx])]
    name = path.splitext(fLists[expIx][0].split('/')[-1])[0][:-4]
    # Export plots --------------------------------------------------------
    exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        transparent=transparent, vLines=vLines, hLines=hLines
    )
    return None


def exportTracesPlot(
    tS, nS, STYLE, PATH_IMG, append='', 
    vLines=[0, 0], hLines=[0], labelPos=(.7, .9), autoAspect=False,
    border=True, borderColor='#8184a7AA', borderWidth=2, popScaler=1,
    wop=0, wopPrint=True, cpt=0, cptPrint=False, poe=0, poePrint=False,
    transparent=False
):
    if transparent:
        plt.rcParams.update({
            "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),
            "axes.facecolor":    (0.0, 1.0, 0.0, 0.0),
            "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),
        })
    figArr = monet.plotNodeTraces(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1] * popScaler)
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    if autoAspect:
        axTemp.set_aspect(aspect=monet.scaleAspect(STYLE["aspect"], STYLE))
    else:
        axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.axes.xaxis.set_visible(False)
    axTemp.axes.yaxis.set_visible(False)
    # axTemp.xaxis.set_tick_params(width=0)
    # axTemp.yaxis.set_tick_params(width=0)
    axTemp.set_axis_off()
    # axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    # axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))


    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.2, zorder=10, ls='-', lw=.15, color='#000000')
     
    #axTemp.tick_params(color=(0, 0, 0, 0.5))
    axTemp.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    # extent = axTemp.get_tightbbox(figArr[0]).transformed(figArr[0].dpi_scale_trans.inverted())
    if border:
        axTemp.set_axis_on()
        plt.setp(axTemp.spines.values(), color=borderColor)
        pad = 0.025
        for axis in ['top','bottom','left','right']:
            axTemp.spines[axis].set_linewidth(borderWidth)
    else:
        pad = 0
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None,
            orientation='portrait', format='png', 
            transparent=transparent, bbox_inches='tight', pad_inches=pad
        )
    plt.clf()
    plt.cla() 
    plt.close('all')
    plt.gcf()
    return None