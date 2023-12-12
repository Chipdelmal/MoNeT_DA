#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import math
import numpy as np
from os import path
from glob import glob
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
import warnings
warnings.filterwarnings("ignore")


XP_ID = 'TPP'
###############################################################################
# System Constants
###############################################################################
(OVW, JOB_DSK, JOB_SRV) = (True, 30, 80)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Releases and Populations
###############################################################################
(REL_START, RELEASES) = (0, [365*2+(7*i) for i in range(20)])
(POP_SIZE, HUM_SIZE, INC_SIZE, XRAN, FZ) = (
    5e3, 1e3, 1000*1.25,
    (0, 2190), 
    False
)
(STABLE_T, MLR, SAMP_RATE) = (0, False, 1)
MAX_REPS = 100
###############################################################################
# Files and DA constants
###############################################################################
(XP_PTRN, NO_REL_PAT) = ('E_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00')
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
# Data Analysis ---------------------------------------------------------------
(DATA_HEAD, DATA_SCA, DATA_PAD, DATA_TYPE) = (
    (
        ('i_shc', 1), ('i_sbc', 2), 
        ('i_hdr', 3), ('i_rgr', 4),
        ('i_inf', 5),
        ('i_grp', 7)
    ),
    {
        'i_shc': 1e3, 'i_sbc': 1e3, 
        'i_hdr': 1e3, 'i_rgr': 1e5,
        'i_inf': 1e5,
        'i_grp': 1e0
    },
    {
        'i_shc': 5, 'i_sbc': 5, 
        'i_hdr': 5, 'i_rgr': 7,
        'i_inf': 7,
        'i_grp': 2
    },
    {
        'i_shc': np.double, 'i_sbc': np.double, 
        'i_hdr': np.double, 'i_rgr': np.double,
        'i_inf': np.double,
        'i_grp': np.double
    }
)
(THI, THO, THW, TAP) = (
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [0, 365]
)
# REF_FILE = 'E_'+'_'.join(['0'*i for i in list(DATA_PAD.values())[:-1]])
REF_FILE = 'E_01000_01000_00000_0000000_0000000'
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
        cmap = colorPaletteFromHexList(['#ffffff00', '#2614ed66'])
    else:
        cmap = colorPaletteFromHexList(['#ffffff00', '#3b479dCC'])
    return (scalers, HD_DEP, IND_RAN, cmap)

###############################################################################
# Experiments
###############################################################################
def getExps():
    return ('A', 'B')

AGE_DISTR = np.array([192, 294, 269, 120, 82, 44])
AGE_DISTR_N = AGE_DISTR/np.sum(AGE_DISTR)
def getPops(LND):
    if LND=='Kenya':
        NH = 1000 # 55573110
        NM = int(50e6*2.5)
    else:
        NH = 1000 # 23497691 
        NM = int(125e6*2.5)
    return (NH, NM)

###############################################################################
# Names and patterns
###############################################################################
def patternForReleases(ren, AOI, ftype, ext='bz', pad=0):
    renP = str(ren).rjust(pad, '0')
    strPat = XP_PTRN.format(
        '*', '*', '*', '*', '*',
        AOI, '*', ftype, ext
    )
    return strPat

def splitExpNames(PATH_OUT, ext='bz'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))

def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.bz'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids

###############################################################################
# Paths
###############################################################################
def selectPath(USR, LND, EXP):
    if USR == 'zelda':
        PATH_ROOT = f'/RAID5/marshallShare/ReplacementTPP/{LND}/{EXP}/'
    elif USR == 'dsk':
        PATH_ROOT = f'/RAID5/marshallShare/ReplacementTPP/{LND}/{EXP}/'
    (PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT), 
        '{}'.format(PATH_ROOT)
    )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


def landSelector():
    PAN = ([0], )
    return PAN


def getHumanRange(AOI):
    if AOI == 'MRT':
        YRAN = 1e-2
    elif AOI == 'CSS':
        YRAN = 1e-3
    else:
        YRAN = 1
    return YRAN
        


def replaceExpBase(tracePath, refFile):
    head = '/'.join(tracePath.split('/')[:-1])
    tail = tracePath.split('-')[-1]
    return '{}/{}-{}'.format(head, refFile, tail)


def chunks(l, n):
    (d, r) = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]

###############################################################################
# Epi
###############################################################################
def findEpiGroupsIndices(genotypes, classID, groupsList):
    fMatches = []
    for grp in groupsList:
        matches = [s for s in genotypes if (classID+grp)==s]
        fMatches.extend(matches)
    ixMatches = [genotypes.index(m) for m in fMatches]
    return ixMatches

def humanGroupsToGeneDict(statDict, strata, genotypes):
    hDict = {}
    for k in statDict:
        elms = statDict[k]
        # Get the indices from all the elements in the group
        grp = []
        for e in elms:
            grp.extend(findEpiGroupsIndices(genotypes, e, strata))
        # Add to the dictionary with group ID
        hDict[k] = grp
    return hDict


###############################################################################
# Plots
###############################################################################
def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1,
            transparent=True, sampRate=1, ticksHide=True
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        vLines=vLines, transparent=transparent, sampRate=sampRate,
        hLines=hLines, ticksHide=ticksHide
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
    tti=0, ttiPrint=False,
    tto=0, ttoPrint=False,
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
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.1, facecolor='#3687ff', zorder=-10)
        axTemp.axvline(vLines[0], alpha=0.0, ls='-', lw=.1, color='#3687ff', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.0, ls='-', lw=.1, color='#3687ff', zorder=0)

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] > vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#FF5277', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.5, ls='-', lw=.1, color='#FF1A4B', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.5, ls='-', lw=.1, color='#FF1A4B', zorder=0)

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
    if ttiPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*1, 'TTI: {:d}'.format(int(tti)),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        ) 
    if ttoPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*2, 'TTO: {:d}'.format(int(tto)),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        ) 
    if cptPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*3, 'CPT: {:.2f}'.format(cpt),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )         
    if mnfPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*4, 'MIN: {:.2f}'.format(mnf),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )     
    if poePrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*5, 'POE: {:.2f}'.format(poe),
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
    STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*popScaler)
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
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
        ttiPrint=True, ttoPrint=True,
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
        tti=tti, ttiPrint=ttiPrint,
        tto=tto, ttoPrint=ttoPrint,
        ticksHide=ticksHide, transparent=True, 
        sampRate=sampRate, labelspacing=labelspacing
    )
    return None

###############################################################################
# Epi Numbers
###############################################################################
def windowAggregate(dynsArray, window=30, aggFun=sum):
    (delta, dayTotal) = (window, dynsArray.shape[0])
    steps = math.floor(dayTotal/delta)
    # Iterate through array
    (day0, dayF, wCases) = (0, delta, [])
    for _ in range(steps):
        aggCases = aggFun(dynsArray[day0:dayF])
        wCases.append(aggCases)
        (day0, dayF) = (day0+delta, dayF+delta)
    return wCases
