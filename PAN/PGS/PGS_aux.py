#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from numpy import random
from glob import glob
from more_itertools import locate
from os import path
import compress_pickle as pkl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
import warnings
warnings.filterwarnings("ignore")


XP_ID = 'PGS'
###############################################################################
# System Constants
###############################################################################
(OVW, JOB_DSK, JOB_SRV) = (True, 4, 60)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
###############################################################################
# Releases and Populations
###############################################################################
(REL_START, RELEASES) = (50, [365+(7*i) for i in range(10)])
(POP_SIZE, HUM_SIZE, INC_SIZE, XRAN, FZ) = (
    5e3, 1e3, 1000*1.25,
    (REL_START, 5*int(365)), 
    False
)
(STABLE_T, MLR, SAMP_RATE) = (0, False, 1)
MAX_REPS = 200
###############################################################################
# Sensitivity Analysis
###############################################################################
SA_SAMPLES = 2**14*2
SA_RANGES = (
    ('ren', (1, 48)), 
    ('rer', (1, 50)), 
    ('rei', (1, 15)),
    ('pct', (.75, 1)), 
    ('pmd', (.75, 1)), 
    ('mfr', (0, .25)), 
    ('mtf', (.5, 1)), 
    ('fvb', (0, .25))
)
###############################################################################
# Files and DA constants
#   "ren", "rer", "rei", "pct", "pmd", "mfr", "mtf", "fvb"
#   1e0, 1e8, 1e0, 1e10, 1e10, 1e10, 1e10, 1e10
#   4, 14, 4, 12, 12, 12, 12, 12
###############################################################################
(XP_PTRN, NO_REL_PAT) = ('E_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}', '00')
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
# Data Analysis ---------------------------------------------------------------
(DATA_HEAD, DATA_SCA, DATA_PAD, DATA_TYPE) = (
    (
        ('i_ren', 1), ('i_res', 2), ('i_rei', 3),
        ('i_pct', 4), ('i_pmd', 5), 
        ('i_mfr', 6), ('i_mtf', 7), ('i_fvb', 8),
        ('i_grp', 10)
    ),
    {
        'i_ren': 1e0,  'i_res': 1e8, 'i_rei': 1e0,
        'i_pct': 1e10, 'i_pmd': 1e10, 
        'i_mfr': 1e10, 'i_mtf': 1e10, 'i_fvb': 1e10,
        'i_grp': 1e0
    },
    {
        'i_ren': 4,  'i_res': 14, 'i_rei': 4,
        'i_pct': 12, 'i_pmd': 12, 
        'i_mfr': 12, 'i_mtf': 12, 'i_fvb': 12,
        'i_grp': 2
    },
    {
        'i_ren': np.int8,   'i_res': np.double, 'i_rei': np.int8,
        'i_pct': np.double, 'i_pmd': np.double, 
        'i_mfr': np.double, 'i_mtf': np.double, 'i_fvb': np.double,
        'i_grp': np.int8
    }
)
(THI, THO, THW, TAP) = (
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [.10, .20, .25, .50, .75, .80, .90],
    [0, 365]
)
# REF_FILE = 'E_0000_00000000000000_0000_000000000000_000000000000_000000000000_000000000000_000000000000'
REF_FILE = 'E_'+'_'.join(['0'*i for i in list(DATA_PAD.values())[:-1]])
###############################################################################
# DICE Plots
###############################################################################
pFeats = (
    ('i_ren', 'linear'), ('i_res', 'linear'), ('i_rei', 'linear'),
    ('i_pct', 'linear'), ('i_pmd', 'linear'),
    ('i_mfr', 'linear'), ('i_mtf', 'linear'), ('i_fvb', 'linear'),
)
DICE_PARS = (
    ('CPT', 0.005, '#4361ee43', (0, 1)),
    ('WOP', 0.050, '#be0aff33', (0, 5*365+50)),
    ('TTO', 0.050, '#9ef01a33', (0, 5*365+50)),
    ('TTI', 0.075, '#23194233', (0, 150)),
    ('MNF', 0.000, '#00B3E643', (0, 1)),
    ('POE', 0.001, '#ff006e22', (0, 1))
)
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
        cmap = colorPaletteFromHexList(['#ffffff00', '#3687ff33'])
    elif MOI == 'CPT':
        cmap = colorPaletteFromHexList(['#ffffff00', '#2614ed55'])
    elif MOI == 'POE':
        cmap = colorPaletteFromHexList(['#ffffff00', '#8338EC55'])
    else:
        cmap = colorPaletteFromHexList(['#ffffff00', '#3b479d55'])
    return (scalers, HD_DEP, IND_RAN, cmap)

###############################################################################
# Experiments
###############################################################################
def getExps():
    return ('A', 'B')

###############################################################################
# Names and patterns
###############################################################################
def patternForReleases(ren, AOI, ftype, ext='bz', pad=0):
    renP = str(ren).rjust(pad, '0')
    strPat = XP_PTRN.format(
        renP, '*', '*', '*', '*', '*', '*', '*', 
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
def selectPath(USR, DRV=None):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/pgSIT2/{}/'.format(DRV)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/pgSIT2/{}/'.format(DRV)
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
    # ax.vlines(
    #     xLvls, 0, 1, lw=gw, ls='--', color='#000000', 
    #     transform=ax.get_xaxis_transform(), zorder=-1
    # )
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
    fig.savefig(fName, dpi=dpi, bbox_inches='tight')
    plt.clf(); plt.cla(); plt.close('all'); plt.gcf()
    return None

TREE_COLS = [
    '#2614ed', '#FF006E', '#45d40c', '#8338EC', '#1888e3', 
    '#BC1097', '#FFE93E', '#3b479d', '#540d6e', '#7bdff2'
]




###############################################################################
# Dev for ML
###############################################################################
def initDFsForML(
            fPaths, header, thiS, thoS, thwS, ttpS, maxReps,
            peak=['min', 'minx', 'max', 'maxx'],
            POE=True, poe=['POE', 'POF'],
            CPT=True, cpt=['CPT'], der=['DER']
        ):
    fNum = len(fPaths)*maxReps
    if (POE and not CPT):
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, poe)]
    elif (CPT and not POE): 
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, cpt)]
    elif (POE and CPT):
        heads = [
            list(header)+i for i in (
                thiS, thoS, thwS, ttpS, peak, poe, cpt, der
            )
        ]
    else:
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak)]
    DFEmpty = [pd.DataFrame(int(0), index=range(fNum), columns=h) for h in heads]
    return DFEmpty

def pstProcessParallelML(
        exIx, header, xpidIx, maxReps, sampRate=1, offset=0,
        thi=.25, tho=.25, thw=.25, tap=50, thp=(.025, .975),
        finalDay=-1, qnt=0.5, CPT=True,
        DF_SORT=['TTI', 'TTO', 'WOP', 'MIN', 'MAX', 'CPT']
    ):
    (outPaths, fPaths) = exIx
    (fNum, digs) = monet.lenAndDigits(fPaths)
    ###########################################################################
    # Setup dataframes
    ###########################################################################
    outDFs = initDFsForML(fPaths, header, thi, tho, thw, tap, maxReps)[:-1]
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    fmtStr = '{}+ File: {}/{}'
    rowWrite = 0
    for (i, fPath) in enumerate(fPaths):
        repRto = np.load(fPath)
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND), 
            end='\r'
        )
        #######################################################################
        # Calculate Metrics
        #######################################################################
        mtrsReps = monet.calcMetrics(repRto, thi=thi, tho=tho, thw=thw, tap=tap)
        #######################################################################
        # Reshapes
        #######################################################################
        mtrsNames = list(mtrsReps.keys())
        mtrsDict = {
            'TTI': np.asarray(mtrsReps['TTI']).T,
            'TTO': np.asarray(mtrsReps['TTO']).T,
            'WOP': np.asarray(mtrsReps['WOP']).T,
            'CPT': np.asarray([mtrsReps['CPT']]).T,
            'MIN': np.asarray(mtrsReps['MIN']).T,
            'MAX': np.asarray(mtrsReps['MAX']).T
        }
        repsNum = np.asarray(mtrsReps['CPT']).T.shape[0]
        #######################################################################
        # Update in Dataframes
        #######################################################################
        xpid = monet.getXpId(fPath, xpidIx)
        for repIx in range(repsNum):
            mtrs = [mtrsDict[k][repIx] for k in DF_SORT]
            updates = [xpid + mt.tolist() for mt in mtrs]
            outDFs[0].iloc[rowWrite] = updates[0] # TTI
            outDFs[1].iloc[rowWrite] = updates[1] # TTO
            outDFs[2].iloc[rowWrite] = updates[2] # WOP
            outDFs[4].iloc[rowWrite] = updates[3][:-2]+updates[3][-2:]+updates[4][-2:] # MIN/MAX
            outDFs[6].iloc[rowWrite] = updates[5] # CPT
            rowWrite = rowWrite + 1
    ###########################################################################
    # Export Data
    ###########################################################################
    outDFs[0].loc[~(outDFs[0]==0).all(axis=1)].to_csv(outPaths[0], index=False)
    outDFs[1].loc[~(outDFs[0]==0).all(axis=1)].to_csv(outPaths[1], index=False)
    outDFs[2].loc[~(outDFs[0]==0).all(axis=1)].to_csv(outPaths[2], index=False)
    outDFs[4].loc[~(outDFs[0]==0).all(axis=1)].to_csv(outPaths[4], index=False)
    outDFs[6].loc[~(outDFs[0]==0).all(axis=1)].to_csv(outPaths[6], index=False)
    return None


def getSASortedDF(df, column, sortingLabels, normalized=True):
    srtNames = [i.replace('i_', '') for i in sortingLabels]
    srtNames = list(map(lambda x: x.replace('rer', 'res'), srtNames))
    try:
        # SA dataframes -------------------------------------------------------
        names = list(df['names'])
        names = list(map(lambda x: x.replace('rer', 'res'), names))
    except:
        # ML dataframes -------------------------------------------------------
        names = list(df['Feature'])
        names = [i.replace('i_', '') for i in names]
    sortIx = [names.index(lbl) for lbl in srtNames]
    # Calculate return --------------------------------------------------------
    if normalized:
        norms = df[column]/np.nansum(df[column])
    else:
        norms = df[column]
    # Return sorted -----------------------------------------------------------
    srtSA = [norms[ix] for ix in sortIx]
    return srtSA


def adjRSquared(rSquared, samplesNum, featuresNum):
    rAdj = 1-(1-rSquared)*(samplesNum-1)/(samplesNum-featuresNum-1)
    return rAdj


def unison_shuffled_copies(a, b, size=1000):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p][:size], b[p][:size]