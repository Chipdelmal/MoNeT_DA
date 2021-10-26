
from math import exp
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import MoNeT_MGDrivE as monet


MKRS = ('o', '^', 's', 'p', 'd')
MCOL = ('#e0c3fc', '#bdb2ff', '#a0c4ff', '#ffd6a5')
RVB = monet.colorPaletteFromHexList(['#ffffff',  '#9b5de5', '#00296b'])


def selectPaths(USR):
    if USR=='lab':
        (PT_DTA, PT_IMG) = (
            '/Volumes/marshallShare/Mov/dta',
            '/Volumes/marshallShare/Mov/trp'
        )
    elif USR=='dsk':
        (PT_DTA, PT_IMG) = (
            '/home/chipdelmal/Documents/WorkSims/Mov/dta',
            '/home/chipdelmal/Documents/WorkSims/Mov/trp'
        )
    return (PT_DTA, PT_IMG)


def unifyTransitionsMatrix(BB, BQ, QB, QQ):
    (n, m) = (BB.shape[0], QQ.shape[0])
    psi = np.empty((n+m, n+m))
    # BB Section --------------------------------------------------------------
    for i in range(n):
        for j in range(n):
            psi[i, j] = BB[i, j]
    # BQ Section --------------------------------------------------------------
    for i in range(n):
        for j in range(m):
            psi[i, j + n] = BQ[j, i]
    # QB Section --------------------------------------------------------------
    for i in range(n):
        for j in range(m):
            psi[j+n, i] = QB[i, j]
    # QQ Section --------------------------------------------------------------
    for i in range(m):
        for j in range(m):
            psi[i+n, j+n] = QQ[i, j]
    return psi


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


def plotNetwork(
    fig, ax, mtxTransitions, ptsB, ptsA, size,
    c='#dd5fb', lw=.3, la=5, arrows=False, hw=.05, hl=0.1,
    alpha=.75
):
    (aNum, bNum) = (ptsA.shape[0], ptsB.shape[0])
    for j in range(aNum):
        src = ptsA[j]
        for i in range(bNum):
            snk = ptsB[i]
            if not arrows:
                plt.plot(
                    [src[0], snk[0]], [src[1], snk[1]],
                    lw=math.log(1+lw*mtxTransitions[j][i]),
                    alpha=min(alpha, math.log(1+la*mtxTransitions[j][i])),
                    solid_capstyle='round', c=c,
                    zorder=0
                )
            else:
                (dx, dy)= ((src[0]-snk[0]), (src[1]-snk[1]))
                scl=size[j]/math.sqrt(dx**2+dy**2)
                plt.arrow(
                    snk[0], snk[1], dx-dx*hl*1.2, dy-dy*hl*1.2,
                    lw=math.log(1+lw*mtxTransitions[j][i]),
                    alpha=min(alpha, math.log(1+la*mtxTransitions[j][i])),
                    head_width=hw, head_length=hl, fc=c, ec=c,
                    zorder=0, shape='left'
                )
    return (fig, ax)


