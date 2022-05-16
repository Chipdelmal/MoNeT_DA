
import math
from os import path
import numpy as np
from numpy import random
import compress_pickle as pkl
import matplotlib.pyplot as plt
from more_itertools import locate
import MoNeT_MGDrivE as monet
import matplotlib.colors as mcolors
from sklearn.preprocessing import LabelBinarizer
# from mpl_toolkits.basemap import Basemap
import geopandas as geop
from shapely import geometry
from shapely.ops import polygonize
from scipy.spatial import Voronoi
import geopandas as geop
# from matplotlib import cm, colors, colorbar
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore",category=UserWarning)


###############################################################################
# PreProcess Updates
###############################################################################
def preProcessParallel(
            exIx, expNum,
            drive, analysisOI='HLT', prePath='./',
            nodesAggLst=[[0]], fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=False, SPA=False, REP=False, SRP=True,
            sexFilenameIdentifiers={"male": "M_", "female": "F_"}
        ):
    (ix, expDirsMean, expDirsTrac) = exIx
    monet.printProgress(ix+1, expNum, nodeDigits)
    (pathMean, pathTraces) = (expDirsMean, expDirsTrac+'/')
    expName = pathMean.split('/')[-1]
    fNameFmt = '{}/{}-{}_'.format(prePath, expName, analysisOI)
    # Iterate through experiment files and skip errors (unsafe but logs)
    file = open("preProcess.log", "w")
    file.write('# Files with errors!\n')
    file.close()
    try:
        monet.preProcessLandscape(
            pathMean, pathTraces, expName, drive, prePath,
            analysisOI=analysisOI, nodesAggLst=nodesAggLst,
            fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
            SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
            sexFilenameIdentifiers=sexFilenameIdentifiers
        )
    except:
        print('- Failed on: {}'.format(expName))
        file = open("preProcess.log", "a")
        file.write('{}\n'.format(expName))
        file.close()
    return None


###############################################################################
# PreTraces Updates
###############################################################################
def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1, sampRate=1
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    monet.exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        sampRate=sampRate
    )
    return None


###############################################################################
# PstTraces Updates
###############################################################################
def exportPstTracesParallel(
        exIx, expsNum,
        STABLE_T, THS, QNT, STYLE, PT_IMG, 
        border=True, borderColor='#322E2D', borderWidth=1, 
        labelPos=(.7, .9), xpsNum=0, digs=3, 
        autoAspect=False, popScaler=1,
        wopPrint=True, cptPrint=True, poePrint=True, mnfPrint=True, 
        ticksHide=True, transparent=True, sampRate=1, labelspacing=.1
    ):
    (ix, repFile, tti, tto, wop, mnf, _, poe, cpt) = exIx
    repDta = pkl.load(repFile)
    # Print to terminal -------------------------------------------------------
    padi = str(ix+1).zfill(digs)
    fmtStr = '{}+ File: {}/{}'
    print(fmtStr.format(monet.CBBL, padi, expsNum, monet.CEND), end='\r')
    # Traces ------------------------------------------------------------------
    pop = repDta['landscapes'][0][STABLE_T][-1]
    # STYLE['yRange'] = (0,  pop*popScaler)
    monet.exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto, 0], hLines=[mnf*pop], labelPos=labelPos, 
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        autoAspect=autoAspect, popScaler=popScaler,
        wop=wop, wopPrint=wopPrint, 
        cpt=cpt, cptPrint=cptPrint,
        poe=poe, poePrint=poePrint,
        mnf=mnf, mnfPrint=mnfPrint,
        ticksHide=ticksHide, transparent=True, 
        sampRate=sampRate, labelspacing=labelspacing
    )
    return None


def exportTracesPlot(
    tS, nS, STYLE, PATH_IMG, append='', 
    vLines=[0, 0], hLines=[0], labelPos=(.7, .95), autoAspect=False,
    border=True, borderColor='#8184a7AA', borderWidth=2, popScaler=1,
    wop=0, wopPrint=True, 
    cpt=0, cptPrint=False, 
    poe=0, poePrint=False,
    mnf=0, mnfPrint=False,
    transparent=False, ticksHide=True, sampRate=1,
    fontsize=5, labelspacing=.1
):
    if transparent:
        plt.rcParams.update({
            "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),
            "axes.facecolor":    (0.0, 1.0, 0.0, 0.0),
            "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),
        })
    figArr = monet.plotNodeTraces(tS, STYLE, sampRate=sampRate)
    axTemp = figArr[0].get_axes()[0]
    STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*popScaler)
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    if autoAspect:
        axTemp.set_aspect(aspect=monet.scaleAspect(STYLE["aspect"], STYLE))
    else:
        axTemp.set_aspect(aspect=STYLE["aspect"])
    if ticksHide:
        axTemp.axes.xaxis.set_ticklabels([])
        axTemp.axes.yaxis.set_ticklabels([])
        axTemp.axes.xaxis.set_visible(False)
        axTemp.axes.yaxis.set_visible(False)
        axTemp.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        axTemp.set_axis_off()
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    
    days = tS['landscapes'][0].shape[0]*sampRate
    print([vLines, wop, days])

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] < vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#3687ff', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-.', lw=.35, color='#3687ff', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-.', lw=.35, color='#3687ff', zorder=0)

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] > vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#FF5277', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-.', lw=.35, color='#FF1A4B', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-.', lw=.35, color='#FF1A4B', zorder=0)

    for hline in hLines:
        axTemp.axhline(hline, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000')
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.25, zorder=10, ls='--', lw=.35, color='#000000')
    # Print metrics -----------------------------------------------------------
    if  wopPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*0, 'WOP: '+str(int(wop)),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )
    if cptPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*1, 'CPT: {:.3f}'.format(cpt),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )    
    if poePrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*2, 'POE: {:.3f}'.format(poe),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )        
    if mnfPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*3, 'MIN: {:.3f}'.format(mnf),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )     
    # --------------------------------------------------------------------------
    #axTemp.tick_params(color=(0, 0, 0, 0.5))
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


###############################################################################
# PstFraction Updates
###############################################################################
def pstFractionParallel(exIx, PT_OUT):
    (_, bFile, mFile, tFile) = exIx
    # Load data ---------------------------------------------------------------
    (base, trace) = [pkl.load(file) for file in (bFile, tFile)]
    # Process data ------------------------------------------------------------
    fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
    repsRatios = monet.getPopRepsRatios(base, trace, 1)
    np.save(fName, repsRatios)
    return None


###############################################################################
# PstProcess Updates
###############################################################################
def calcMetrics(
        repRto, 
        sampRate=1, offset=0,
        thi=.25, tho=.25, thw=.25, tap=50, thp=(.025, .975),
        finalDay=-1
    ):
    (minS, maxS, _, _) = monet.calcMinMax(repRto)
    mtrRep = {
        'TTI': monet.calcTTI(repRto, thi, sampRate=sampRate, offset=offset),
        'TTO': monet.calcTTO(repRto, tho, sampRate=sampRate, offset=offset),
        'WOP': monet.calcWOP(repRto, thw, sampRate=sampRate),
        'MIN': minS, 'MAX': maxS,
        'RAP': monet.getRatioAtTime(repRto, tap, sampRate=sampRate),
        'POE': monet.calcPOE(repRto, finalDay=finalDay, thresholds=thp),
        'CPT': monet.calcCPT(repRto)
    }
    return mtrRep



def calcMtrQnts(mtrsReps, qnt=0.5):
    ttiSQ = [np.nanquantile(tti, qnt) for tti in mtrsReps['TTI']]
    ttoSQ = [np.nanquantile(tto, 1-qnt) for tto in mtrsReps['TTO']]
    wopSQ = [np.nanquantile(wop, 1-qnt) for wop in mtrsReps['WOP']]
    rapSQ = [np.nanquantile(rap, qnt) for rap in mtrsReps['RAP']]
    mniSQ = (
        np.nanquantile(mtrsReps['MIN'][0], qnt), 
        np.nanquantile(mtrsReps['MIN'][1], qnt)
    )
    mnxSQ = (
        np.nanquantile(mtrsReps['MAX'][0], qnt), 
        np.nanquantile(mtrsReps['MAX'][1], 1-qnt)
    )
    cptSQ = (np.nanquantile(mtrsReps['CPT'], qnt))
    poeSQ = [mtrsReps['POE']]
    # Setup return dictionary -------------------------------------------------
    mtrQnt = {
        'TTI': ttiSQ,
        'TTO': ttoSQ,
        'WOP': wopSQ,
        'RAP': rapSQ,
        'MIN': list(mniSQ)+list(mnxSQ),
        'POE': list(poeSQ[0]),
        'CPT': [cptSQ]
    }
    return mtrQnt


def pstProcessParallel(
        exIx, header, xpidIx, sampRate=1, offset=0,
        thi=.25, tho=.25, thw=.25, tap=50, thp=(.025, .975),
        finalDay=-1, qnt=0.5, POE=True, CPT=True,
        DF_SORT=['TTI', 'TTO', 'WOP', 'RAP', 'MIN', 'POE', 'CPT']
    ):
    (outPaths, fPaths) = exIx
    (fNum, digs) = monet.lenAndDigits(fPaths)
    ###########################################################################
    # Setup dataframes
    ###########################################################################
    outDFs = monet.initDFsForDA(
        fPaths, header, 
        thi, tho, thw, tap, POE=POE, CPT=CPT
    )[:-1]
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    fmtStr = '{}+ File: {}/{}'
    (i, fPath) = (0, fPaths[0])
    for (i, fPath) in enumerate(fPaths):
        repRto = np.load(fPath)
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND), 
            end='\r'
        )
        #######################################################################
        # Calculate Metrics
        #######################################################################
        mtrsReps = calcMetrics(
            repRto, sampRate=sampRate, offset=offset,
            thi=thi, tho=tho, thw=thw, tap=tap
        )
        # print(mtrsReps['TTI'])
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        mtrsQnt = calcMtrQnts(mtrsReps, qnt)
        #######################################################################
        # Update in Dataframes
        #######################################################################
        (xpid, mtrs) = (
            monet.getXpId(fPath, xpidIx),
            [mtrsQnt[k] for k in DF_SORT]
        )
        updates = [xpid+i for i in mtrs]
        for (df, entry) in zip(outDFs, updates):
            df.iloc[i] = entry
    ###########################################################################
    # Export Data
    ###########################################################################
    for (df, pth) in zip(outDFs, outPaths):
        df.to_csv(pth, index=False)


###############################################################################
# DICE Plots
###############################################################################
def plotDICE(
        dataEffect, xVar, yVar, features, hRows={},
        sampleRate=1, wiggle=False, sd=0, scale='linear', 
        lw=.175, color='#be0aff13', hcolor='#000000', hlw=.175,
        rangePad=(.975, 1.025), gw=.25, yRange=None, ticksHide=False
    ):
    (inFact, outFact) = (dataEffect[features], dataEffect[yVar])
    # Get levels and factorial combinations without feature -------------------
    xLvls = sorted(list(inFact[xVar].unique()))
    dropFeats = inFact.drop(xVar, axis=1).drop_duplicates()
    dropSample = dropFeats.sample(frac=sampleRate)
    # dropIndices = dropSample.index
    # Generate figure ---------------------------------------------------------
    doneRows = set()
    (fig, ax) = plt.subplots(figsize=(10, 10))
    # Log and linear scales ---------------------------------------------------
    if scale == 'log':
        xRan = [xLvls[1], xLvls[-1]]
        xdelta = .125
    else:
        xRan = [xLvls[0], xLvls[-1]]
        xdelta = (xRan[1] - xRan[0])/100
    if yRange is None:
        yRan = [min(dataEffect[yVar]), max(dataEffect[yVar])]
    else:
        yRan = yRange
    # Iterate through traces --------------------------------------------------
    for i in range(0, dropSample.shape[0]):
        # If the row index has already been processed, go to the next ---------
        if (dropSample.iloc[i].name) in doneRows:
            continue
        # If not, process and plot --------------------------------------------
        entry = dropSample.iloc[i]
        zipIter = zip(list(entry.keys()), list(entry.values))
        fltrRaw = [list(dataEffect[col]==val) for (col, val) in zipIter]
        fltr = [all(i) for i in zip(*fltrRaw)]
        rowsIx = list(locate(fltr, lambda x: x == True))
        [doneRows.add(i) for i in rowsIx]
        # With filter in place, add the trace ---------------------------------
        data = dataEffect[fltr][[xVar, yVar]]
        if wiggle:
            yData = [i+random.uniform(low=-sd, high=sd) for i in data[yVar]]
        else:
            yData = data[yVar]
        # Plot markers --------------------------------------------------------
        if len(hRows) != 0:
            for (ix, r) in enumerate(list(data.index)):
                # Draw highlights ---------------------------------------------
                (x, y) = (data[xVar].iloc[ix], yData[ix])
                if scale == 'log':
                    xPoint = [x*(1-xdelta), x, x*(1+xdelta)]
                else:
                    xPoint = [x-xdelta, x, x+xdelta]
                yD = (yRan[1]-yRan[0])/100
                if r in hRows:
                    (c, yD) = (hcolor, yD)
                    ax.plot(xPoint, [y+yD, y, y+yD], color=c, lw=hlw, zorder=10)
                # else:
                #     (c, yD) = (color, -yD)
                # ax.plot(xPoint, [y+yD, y, y+yD], color=c, lw=hlw, zorder=10)
        # Plot trace ----------------------------------------------------------
        ax.plot(data[xVar], yData, lw=lw, color=color)
    # Styling -----------------------------------------------------------------
    if yRange is None:
        STYLE = {
            'xRange': xRan,
            'yRange': [min(outFact)*rangePad[0], max(outFact)*rangePad[1]]
        }
    else:
        STYLE = {
            'xRange': xRan,
            'yRange': yRan
        }
    # Apply styling to axes ---------------------------------------------------
    if ticksHide:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        # axTemp.xaxis.set_tick_params(width=0)
        # axTemp.yaxis.set_tick_params(width=0)
        ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        ax.set_axis_off()
    # ax.set_aspect(monet.scaleAspect(1, STYLE))
    ax.set_xlim(STYLE['xRange'])
    ax.set_ylim(STYLE['yRange'])
    ax.set_xscale(scale)
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax.vlines(
        xLvls, 0, 1, lw=gw, ls='--', color='#000000', 
        transform=ax.get_xaxis_transform(), zorder=-1
    )
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20, rotation=90)
    fig.tight_layout()
    return (fig, ax)


def exportDICEParallel(
        AOI, xVar, yVar, dataSample, FEATS, PT_IMG, hRows={}, 
        dpi=500, lw=0.175, scale='linear', wiggle=False, sd=0.1, 
        color='blue', sampleRate=0.5, hcolor='#00000020', hlw=5,
        yRange=None, ticksHide=False
    ):
    prgStr = '{}* Processing [{}:{}:{}]{}'
    print(prgStr.format(monet.CBBL, AOI, yVar, xVar, monet.CEND), end='\r')
    fName = path.join(PT_IMG, 'DICE_{}_{}.png'.format(xVar[2:], yVar))
    (fig, ax) = plotDICE(
        dataSample, xVar, yVar, FEATS, hRows=hRows, lw=lw,
        scale=scale, wiggle=wiggle, sd=sd, color=color,
        sampleRate=sampleRate, hcolor=hcolor, hlw=hlw, yRange=yRange,
        ticksHide=ticksHide
    )
    fig.savefig(fName, dpi=dpi, bbox_inches='tight', pad=0)
    plt.clf(); plt.cla(); plt.close('all'); plt.gcf()
    return None


###############################################################################
# Auxiliary
###############################################################################
def chunks(l, n):
    (d, r) = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]


def releasedSex(reType):
    if reType==1:
        return (1, 0, 0)
    elif reType==2:
        return (0, 1, 0)
    elif reType==3:
        return (0, 0, 1)
    else:
        return False

###############################################################################
# ML
###############################################################################
class Binarizer(LabelBinarizer):
    def transform(self, y):
        Y = super().transform(y)
        if self.y_type_ == 'binary':
            return np.hstack((Y, 1-Y))
        else:
            return Y

    def inverse_transform(self, Y, threshold=None):
        if self.y_type_ == 'binary':
            return super().inverse_transform(Y[:, 0], threshold)
        else:
            return super().inverse_transform(Y, threshold)

###############################################################################
# Plots
###############################################################################

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


def replaceExpBase(tracePath, refFile):
    head = '/'.join(tracePath.split('/')[:-1])
    tail = tracePath.split('-')[-1]
    return '{}/{}-{}'.format(head, refFile, tail)


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


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



def voronoi_polygons(X, margin=0):
    assert isinstance(X, np.ndarray), 'Expecting a numpy array.'
    assert X.ndim == 2, 'Expecting a two-dimensional array.'
    assert X.shape[1] == 2, 'Number of columns is different from expected.'
    n_points = X.shape[0]

    c1, c2 = np.sort(X[:, 0]), np.sort(X[:, 1])
    _diffs = np.array([max(margin, np.diff(c1).mean()), max(margin, np.diff(c2).mean())])

    min_c1, min_c2 = X.min(0) - _diffs
    max_c1, max_c2 = X.max(0) + _diffs

    extra_points = np.vstack([np.vstack([np.repeat(min_c1, n_points), c2]).T,
                              np.vstack([np.repeat(max_c1, n_points), c2]).T,
                              np.vstack([c1, np.repeat(min_c2, n_points)]).T,
                              np.vstack([c1, np.repeat(max_c2, n_points)]).T])

    _X = np.vstack([X, extra_points])

    # Define polygons geometry based on tessellation
    vor = Voronoi(_X)
    lines = [geometry.LineString(vor.vertices[li]) for li in vor.ridge_vertices if -1 not in li]
    disord = geometry.MultiPolygon(list(polygonize(lines)))
    ix_order = np.array([[i for i, di in enumerate(disord) if di.contains(geometry.Point(pi))]
                         for pi in X]).ravel()

    return geop.GeoDataFrame({'geometry': geometry.MultiPolygon([disord[i] for i in ix_order])})



def regular_polygons(X, radius, n_angles=8):
    assert isinstance(X, np.ndarray), 'Expecting a numpy array.'
    assert X.ndim == 2, 'Expecting a two-dimensional array.'
    assert X.shape[1] == 2, 'Number of columns is different from expected.'

    assert isinstance(n_angles, int), 'n_angles must be an integer.'
    assert n_angles >= 3, 'Angles must be greater than two.'

    vertex = np.pi * np.linspace(0, 2, n_angles + 1)

    if isinstance(radius, float):
        assert radius > 0, 'Radius must be positive.'
        polys = [np.vstack([xi + radius * np.array([np.cos(t), np.sin(t)]) for t in vertex]) for xi in X]
    else:
        assert isinstance(radius, np.ndarray), 'Expecting a numpy array.'
        assert radius.ndim == 1, 'Expecting a one-dimensional array.'
        assert radius.size == X.shape[0], 'Array size is different from expected.'

        polys = [np.vstack([xi + ri * np.array([np.cos(t), np.sin(t)]) for t in vertex]) for xi, ri in zip(X, radius)]

    return geop.GeoDataFrame({'geometry': geometry.MultiPolygon([geometry.Polygon(pi) for pi in polys])})


def disjoint_polygons(X, radius, n_angles=8):
    vorpol = voronoi_polygons(X, margin=2*np.max(radius))
    regpol = regular_polygons(X, radius=radius, n_angles=n_angles)
    dispol = [vi.intersection(pi) for vi,pi in zip(vorpol.geometry, regpol.geometry)]

    return geop.GeoDataFrame({'geometry': geometry.MultiPolygon(dispol)})


def plot_buffer(X, G, title):
    fig, ax = plt.subplots(1, 1, figsize = (8, 8))
    ax.plot(*X.T, marker='o', color='darkred', lw=0)
    ax.set_xlim(-5, 15)
    ax.set_ylim(-5, 15)
    for i, gi in enumerate(G.geometry): # Add continents
        ax.add_patch(PolygonPatch(gi, color='orange', ec='orange', lw=3, alpha=.4))
    ax.set_axis_off()


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
    offset=2.5, amplitude=2, alpha=.35, marker=(6, 0), DPI=500, 
    edgecolor='#ffffff', plotTime=False
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
    if plotTime:
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


def geneCountsToFractions(popCountsArray):
    totalPop = popCountsArray[:, -1]
    geneFractions = [
        zeroDivide(popCountsArray[:, i], totalPop) 
        for i in range(len(popCountsArray[0])-1)
    ]
    geneFractions.append(totalPop)
    return np.asarray(geneFractions).T


def aggCentroids(AGG_lonlats):
    centroids = [(np.mean(i[:, 0]), np.mean(i[:, 1])) for i in AGG_lonlats]
    return np.asarray(centroids)


def zeroDivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def quickSaveFig(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, bbox_inches='tight', pad_inches=.02
     )
