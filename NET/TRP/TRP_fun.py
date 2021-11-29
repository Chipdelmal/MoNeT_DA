
import math
import numpy as np
import networkx as nx
from sklearn.preprocessing import normalize


def expTrapProbability(dist, A=1, b=1):
    prob = A * math.exp(-b * dist)
    return prob


def deleteLoopsFromMatrix(migMat):
    zmat = np.copy(migMat)
    np.fill_diagonal(zmat, 0)
    psiN = normalize(zmat, axis=1, norm='l1')
    return psiN


def placeTrapsRanUnif(trapsNumber, xMinMax, yMinMax):
    traps = np.asarray([
        [
            np.random.uniform(xMinMax[0], xMinMax[1], 1)[0], 
            np.random.uniform(yMinMax[0], yMinMax[1], 1)[0]
        ] for i in range(trapsNumber)
    ])
    return traps


def calcTrapToSitesDistance(trapsXY, sitesXY, dFun=math.dist):
    trapDists = np.asarray([
        [dFun(trap, site) for site in sitesXY]
        for trap in trapsXY
    ]).T
    return trapDists


def calcTrapsSections(
        trapDists, 
        tFun=expTrapProbability, 
        params={
            'Trap':   {'A': .5, 'b': .75},
            'Escape': {'A': 0, 'b': 100}
        }
    ):
    trapProbs = np.asarray([
        [tFun(i, **params['Trap']) for i in dist] 
        for dist in trapDists
    ])
    trapIdentity = np.identity(trapDists.shape[0])
    trapEscape = np.asarray([
        [tFun(i, **params['Escape']) for i in dist] 
        for dist in trapDists
    ]).T
    # Assemble dictionary
    retDict = {
        'Trap': trapProbs, 
        'Identity': trapIdentity,
        'Escape': trapEscape
    }
    return retDict


def assembleTrapMigration(psiN, tProbs):
    (n, m) = (psiN.shape[0], tProbs['Trap'].shape[1])
    tau = np.empty((n+m, n+m))
    # Migration Section -------------------------------------------------------
    B = psiN
    for i in range(n):
        for j in range(n):
            tau[i, j] = B[i, j]
    # Trapped Section ---------------------------------------------------------
    A = tProbs['Trap'].T
    for i in range(n):
        for j in range(m):
            tau[i, j + n] = A[j, i]
    # Escape Section ----------------------------------------------------------
    O = tProbs['Escape'].T
    for i in range(n):
        for j in range(m):
            tau[j+n, i] = O[i, j]
    # Identity Section --------------------------------------------------------
    I = tProbs['Identity']
    for i in range(m):
        for j in range(m):
            tau[i+n, j+n] = I [i, j]
    # Normalize ---------------------------------------------------------------
    tauN = normalize(tau, axis=1, norm='l1')
    # np.apply_along_axis(sum, 1, tauN)
    return tauN


def reshapeInCanonicalForm(tau, sitesN, trapsN):
    canO = list(range(sitesN, sitesN+trapsN))+list(range(0, sitesN))
    tauCan = np.asarray([[tau[i][j] for j in canO] for i in canO])
    return tauCan


def getMarkovAbsorbing(tauCan, trapsN):
    A = tauCan[trapsN:, :trapsN]
    B = tauCan[trapsN:, trapsN:]
    F = np.linalg.inv(np.subtract(np.identity(B.shape[0]), B))
    return F