
import re
import pandas as pd
import numpy as np
import math
from numpy import random
from glob import glob
from more_itertools import locate
from os import path
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
import warnings

# #############################################################################
# Constants
# #############################################################################
(XP_ID, XP_PTRN, EXPS) = (
    'SDP', 'E_{}_{}_{}-{}_{}_{}.{}',
    ('001', '003')
)
(POP_SIZE, XRAN, FZ, STABLE_T) = (25e3, (0, 365*3), True, 0)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT', 'DER'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
DATA_HEAD = (('i_clv', 1), ('i_ren', 2), ('i_res', 3), ('i_grp', 5))
DATA_SCA =  {'i_clv': 1e4, 'i_ren': 1e0, 'i_res': 1e2, 'i_grp': 1e0}
DATA_PAD =  {'i_clv': 4, 'i_ren': 2,  'i_res': 7, 'i_grp': 2}
DATA_TYPE = {'i_clv': np.double, 'i_ren': np.int8, 'i_res': np.double, 'i_grp': np.int8}
(THI, THO, THW, TAP) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i+1)*365-1) for i in range(5)]
    )
(JOB_DSK, JOB_SRV, MLR, SAMP_RATE) = (4, 20, False, 1)

# #############################################################################
# Names and patterns
# #############################################################################
def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def patternForReleases(ren, AOI, ftype, ext='bz'):
    strPat = XP_PTRN.format('*', ren, '*', AOI, '*', ftype, ext)
    return strPat


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.bz'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, DRV, EXP):
    if USR == 'zelda':
        PATH_ROOT = '/RAID5/marshallShare/SplitDrive_Suppression/20230601/{}/{}/'.format(
            DRV, EXP
        )
    elif USR == 'sami':
        PATH_ROOT = '/Users/sanchez.hmsc/Documents/WorkSims/SDP/20230525/{}/{}/'.format(
            DRV, EXP
        )
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)

###############################################################################
# Dependent Variables for Heatmaps
###############################################################################
def colorPaletteFromHexList(clist):
    c = ColorConverter().to_rgba
    clrs = [c(i) for i in clist]
    rvb = LinearSegmentedColormap.from_list("", clrs)
    return rvb

def selectDepVars(MOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP') or (MOI == 'TTO'):
        scalers = [1, 1, XRAN]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'TTI'):
        scalers = [1, 1, XRAN]
        (HD_DEP, IND_RAN) = ('0.1', 7)
    elif (MOI == 'RAP'):
        scalers = [1, 100, 90]
        (HD_DEP, IND_RAN) = ('486', 7)
    elif (MOI == 'MNX'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('min', 7)
    elif (MOI == 'POE'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('POE', 1) 
    elif (MOI == 'CPT'):
        scalers = [1, 100, 1]
        (HD_DEP, IND_RAN) = ('CPT', 1) 
    elif (MOI == 'DER'):
        scalers = [1, 100, 5]
        (HD_DEP, IND_RAN) = ('DER', 5) 
    elif (MOI == 'MNF'):
        scalers = [1, 1, 1]
        (HD_DEP, IND_RAN) = ('MNF', 1) 
    # Color Mapping -----------------------------------------------------------
    if MOI == 'WOP':
        cmap = colorPaletteFromHexList(['#ffffff00', '#7fc8f8DD'])
    elif MOI == 'CPT':
        cmap = colorPaletteFromHexList(['#ffffff00', '#2614ed33'])
    elif MOI == 'POE':
        cmap = colorPaletteFromHexList(['#ffffff00', '#7d7abc88'])
    else:
        cmap = colorPaletteFromHexList(['#ffffff00', '#3b479dCC'])
    return (scalers, HD_DEP, IND_RAN, cmap)

###############################################################################
# Dependent Variables for Heatmaps
###############################################################################
def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1,
            transparent=True, sampRate=1
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        vLines=vLines, transparent=transparent, sampRate=sampRate,
        hLines=hLines
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
        # axTemp.xaxis.set_tick_params(width=0)
        # axTemp.yaxis.set_tick_params(width=0)
        axTemp.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        axTemp.set_axis_off()
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    days = tS['landscapes'][0].shape[0]*sampRate
    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] < vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#3687ff', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-', lw=.1, color='#3687ff', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-', lw=.1, color='#3687ff', zorder=0)

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] > vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#FF5277', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-', lw=.1, color='#FF1A4B', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-', lw=.1, color='#FF1A4B', zorder=0)

    for hline in hLines:
        axTemp.axhline(hline, alpha=.2, zorder=10, ls='-', lw=.15, color='#000000')
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.2, zorder=10, ls='-', lw=.15, color='#000000')
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
    if mnfPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*2, 'MIN: {:.3f}'.format(mnf),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )     
    if poePrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*3, 'POE: {:.3f}'.format(poe),
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

def exportPstTracesParallel(
        exIx, expsNum,
        STABLE_T, THS, QNT, STYLE, PT_IMG, 
        border=True, borderColor='#322E2D', borderWidth=1, 
        labelPos=(.7, .9), xpsNum=0, digs=3, 
        autoAspect=False, popScaler=1,
        wopPrint=True, cptPrint=True, poePrint=True, mnfPrint=True, 
        ticksHide=True, transparent=True, sampRate=1, labelspacing=.1,
        releases=[], hLines=[0]
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
    exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto]+releases, hLines=hLines, labelPos=labelPos, 
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