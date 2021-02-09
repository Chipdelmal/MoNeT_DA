

import numpy as np


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