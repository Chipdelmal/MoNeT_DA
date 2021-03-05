

import numpy as np
import pandas as pd


def zeroDivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def dividePops(n, d):
    return (n / d if d else 0)


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


###############################################################################
# Data Analysis
###############################################################################

def initDFsForDA(
            fPaths, header, thiS, thoS, thwS, ttpS,
            peak=['min', 'minx', 'max', 'maxx'],
            poe=['POE', 'POF'], POE=False
        ):
    fNum = len(fPaths)
    if POE:
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, poe)]
    else:
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak)]
    DFEmpty = [pd.DataFrame(int(0), index=range(fNum), columns=h) for h in heads]
    return DFEmpty


def calcPOE(repRto, finalDay=-1, thresholds=(.025, .975)):
    (reps, days) = repRto.shape
    if finalDay == -1:
        fD = -1
    else:
        fD = finalDay
    fR = [rep[fD] for rep in repRto]
    (loTh, hiTh) = (
        [j < thresholds[0] for j in fR],
        [j > thresholds[1] for j in fR]
    )
    (pLo, pHi) = (sum(loTh)/reps, sum(hiTh)/reps)
    return (pLo, pHi)