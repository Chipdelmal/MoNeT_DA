#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import matplotlib
import pandas as pd
import numpy as np
from glob import glob
import MoNeT_MGDrivE as monet
import compress_pickle as pkl

OVW = True
(JOB_DSK, JOB_SRV) = (2, 20)
XP_NPAT = 'E_{}_{}_{}_{}_{}_{}_{}_{}-{}_{}_{}.{}'
(POP_SIZE, XRAN) = (6e3, (0, 10*365))
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
(DATA_NAMES, DATA_PRE, DATA_PST) = (
    ('TTI', 'TTO', 'WOP', 'RAP', 'MNX', 'POE', 'CPT'),
    ('ECO', 'HLT', 'TRS', 'WLD'), ('HLT', 'TRS', 'WLD')
)
SAMP_RATE = 1
MAX_REPS = 60
EXPS = ('100', )
###############################################################################
# Sensitivity Analysis
###############################################################################
SA_SAMPLES = 2**9
SA_RANGES = (
    ('fcs', (0.000, 1.000)), 
    ('fcb', (0,  )), 
    ('fga', (0.010, 0.100)), 
    ('fgb', (0.425, 0.500)), 
    ('cut', (0.800, 0.950)), 
    ('hdr', (0.600, 0.950)), 
    ('res', (0.001, 0.025)),
    ('ren', (1, ))
)

#   * `fcs`: from=0.05, to=0.95, by=0.05 (1e4)
#   * `fcb`: from=0.05, to=0.95, by=0.05 (1e4)
#   * `fga`: from=0.01, to=0.10, by=0.01 (1e4)
#   * `fgb`: from=0.425, to=0.50, by=0.005 (1e4)
#   * `cut`: from=0.0.80, to=0.95, by=0.05 (1e2)
#   * `hdr`: from=0.60, to=0.95, by=0.05 (1e2)
#   * `ren`: from=0, to=24, by=1 (1e0)
#   * `res`: from=10, to=250, by=0.05 (1e2)

###############################################################################
# Count genotypes
###############################################################################
def countGeneAppearances(genotypes, gene, pos):
    # Split genotypes
    splitGenotypes = [list(genes) for genes in genotypes]
    # Count
    appearances = []
    for p in pos:
        slot = [gene[p] for gene in splitGenotypes]
        matches = re.finditer(gene, ''.join(slot))
        appearances.extend([match.start() for match in matches])
    appearances.sort()
    return appearances


def aggregateGeneAppearances(genotypes, genes):
    gcnt = [countGeneAppearances(genotypes, gn[0], gn[1]) for gn in genes]
    return sorted(flatten(gcnt))


def flatten(l): return [item for sublist in l for item in sublist]


def chunks(l, n):
    (d, r) = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]

###############################################################################
# Data Analysis 
###############################################################################
(DATA_HEAD, DATA_SCA, DATA_PAD) = (
    (
        ('i_fcs', 1), ('i_fcb', 2),
        ('i_fga', 3), ('i_fgb', 4),
        ('i_cut', 5), ('i_hdr', 6),
        ('i_ren', 7), ('i_res', 8)
    ),
    {
        'i_fcs': 1e6, 'i_fcb': 1e6,
        'i_fga': 1e5, 'i_fgb': 1e5,
        'i_cut': 1e6, 'i_hdr': 1e6,
        'i_ren': 1e0, 'i_res': 1e4
    },
    {
        'i_fcs': 6, 'i_fcb': 6,
        'i_fga': 6, 'i_fgb': 6,
        'i_cut': 6, 'i_hdr': 6,
        'i_ren': 2, 'i_res': 4
    }
)
(THI, THO, THW, TAP) = (
    [.10, .15, .20, .25, .50, .75, .80, .85, .90],
    [.10, .15, .20, .25, .50, .75, .80, .85, .90],
    [.10, .15, .20, .25, .50, .75, .80, .85, .90],
    [0, 365]
)
DATA_TYPE = {
    'i_fcs': np.double, 'i_fcb': np.double,
    'i_fga': np.double, 'i_fgb': np.double,
    'i_cut': np.double, 'i_hdr': np.double,
    'i_ren': np.int8,   'i_res': np.double
}
REF_FILE = 'E_'+'_'.join(['0'*i for i in list(DATA_PAD.values())[:-1]])
# #############################################################################
# Paths and Style
# #############################################################################
def selectPath(USR, DRV, EXP):
    if USR == 'srv':
        PATH_ROOT = '/RAID5/marshallShare/tGD/20220926_SA/{}/{}/'.format(DRV, EXP)
    elif USR == 'srv2':
        PATH_ROOT = '/RAID5/marshallShare/tGD/20220602/{}/{}/'.format(DRV, EXP)
    elif USR == 'srv3':
        PATH_ROOT = '/RAID5/marshallShare/tGD/20221030/{}/{}/'.format(DRV, EXP)
    elif USR == 'dsk':
        PATH_ROOT = '/home/chipdelmal/Documents/WorkSims/tGD/{}/{}/'.format(DRV, EXP)
    else:
        print("Username Error!!!!!")
    (PATH_IMG, PATH_DATA) = (
            '{}img/'.format(PATH_ROOT), '{}'.format(PATH_ROOT)
        )
    PATH_PRE = PATH_DATA + 'PREPROCESS/'
    PATH_OUT = PATH_DATA + 'POSTPROCESS/'
    PATH_MTR = PATH_DATA + 'SUMMARY/'
    fldrList = [PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR]
    [monet.makeFolder(i) for i in fldrList]
    return (PATH_ROOT, PATH_IMG, PATH_DATA, PATH_PRE, PATH_OUT, PATH_MTR)


def selectDepVars(MOI, THS, AOI):
    # Select ranges and dependent variable-------------------------------------
    if (MOI == 'WOP'):
        scalers = (1, 1000, round(10*365))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'TTI'):
        scalers = (1, 1000, round(365))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'TTO'):
        scalers = (1, 1000, round(1.75*365))
        (HD_DEP, IND_RAN) = (str(THS), 7)
    elif (MOI == 'RAP'):
        scalers = (1, 1000, 1)
        (HD_DEP, IND_RAN) = ('486', 7)
    elif (MOI == 'MNX'):
        scalers = (1, 1, 1)
        (HD_DEP, IND_RAN) = ('min', 7)
    else:
        scalers = (1, 1, 1)
        (HD_DEP, IND_RAN) = ('min', 7)
    # Color Mapping -----------------------------------------------------------
    if AOI == 'HLT':
        cmap = cmapC
    elif AOI == 'TRS':
        cmap = cmapW
    elif AOI == 'WLD':
        cmap = monet.cmapP
    return (scalers, HD_DEP, IND_RAN, cmap)


def setupFolder(USR, DRV, exp, HD_IND):
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = selectPath(USR, DRV, exp)
    PT_IMG = PT_IMG[:-1]+'Pst/'
    fldrName = '{}_{}/'.format(*HD_IND)
    PT_IMG_XP = PT_IMG+fldrName
    monet.makeFolder(PT_IMG)
    monet.makeFolder(PT_IMG_XP)
    return (PT_ROT, PT_IMG_XP, PT_DTA, PT_PRE, PT_OUT)


def loadDFFromFiles(fName, IND_RAN):
    df = pd.read_csv(fName[0])
    for filename in fName:
        df = df.append(pd.read_csv(filename))
    header = list(df.columns)
    headerInd = header[:IND_RAN]
    return (df, header, headerInd)


def loadDFFromSummary(fName):
    df = pd.read_csv(fName)
    header = list(df.columns)
    indRan = sum([i[0] == 'i' for i in header])
    headerInd = header[:indRan]
    return (df, header, headerInd)


###############################################################################
# Style
###############################################################################
def getStyle(colors, aspectR, xRange, yRange):
    style = {
            "width": .1, "alpha": .1, "dpi": 500,
            "legend": True, "aspect": .5,
            "xRange": xRange, "yRange": yRange,
            "colors": colors
        }
    style['aspect'] = monet.scaleAspect(aspectR, style)
    return style


def axisRange(x):
    return (min(x), max(x))


###############################################################################
# Terminal
###############################################################################
def printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, time, title):
    print(monet.PAD)
    (cred, cwht, cend) = (monet.CRED, monet.CWHT, monet.CEND)
    print(cwht+'MoNeT '+title+' ['+str(time)+']'+cend)
    print(monet.PAD)
    print('{}* Root: {}{}'.format(cred, PATH_ROOT, cend))
    print('{}* Imgs: {}{}'.format(cred, PATH_IMG, cend))
    print('{}* Data: {}{}'.format(cred, PATH_DATA, cend))
    print(monet.PAD)


###############################################################################
# Color Palette
###############################################################################
cdict = {
        'red':  ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.25, 0.25), (1.0, 0.0, 0.0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 0.3, 0.3), (1.0, 0.0, 0.0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 0.25, 0.25))
    }
cmapB = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.95, 0.95)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.4, 0.4))
    }
cmapC = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0, 0)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.65, 0.65)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, .95, .95))
    }
cmapM = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

cdict = {
        'red':      ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.05, 0.05)),
        'green':    ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.91, 0.91)),
        'blue':     ((0.0, 1.0, 1.0), (0.1, 1.0, 1.0), (1.0, 0.06, 0.06))
    }
cmapW = matplotlib.colors.LinearSegmentedColormap('cmapK', cdict, 256)

# [i/256 for i in (14, 235, 16)]


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


def patternForReleases(ren, AOI, ftype, ext='bz', pad=0):
    renP = str(ren).rjust(pad, '0')
    strPat = XP_NPAT.format(
        '*', '*', '*', '*', '*', '*', renP, '*', AOI, '*', ftype, ext
    )
    return strPat


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.lzma'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


def replaceExpBase(tracePath, refFile):
    head = '/'.join(tracePath.split('/')[:-1])
    tail = tracePath.split('-')[-1]
    return '{}/{}-{}'.format(head, refFile, tail)


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
