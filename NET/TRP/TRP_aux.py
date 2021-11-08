
from math import exp
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import MoNeT_MGDrivE as monet


MKRS = ('o', '^', 's', 'p', 'd')
MCOL = ('#e0c3fc', '#bdb2ff', '#a0c4ff', '#ffd6a5')
RVB = monet.colorPaletteFromHexList(['#e0c3fc',  '#00296b'])
# KPARS = {
#     'Trap': {'A': 0.5, 'b': 1},
#     'Escape': {'A': 0, 'b': 100}
# }
KPARS = {
    'Trap': {'A': 0.5, 'b': 0.15},
    'Escape': {'A': 0, 'b': 100}
}
MKERN = [1, 1.0e-10, math.inf]
(DPI, PAD) = (300, 1)

def selectPaths(USR):
    if USR=='lab':
        (PT_DTA, PT_GA, PT_IMG) = (
            '/Volumes/marshallShare/Mov/dta',
            '/Volumes/marshallShare/Mov/GA',
            '/Volumes/marshallShare/Mov/trp',
        )
    elif USR=='dsk':
        (PT_DTA, PT_GA, PT_IMG) = (
            '/home/chipdelmal/Documents/WorkSims/Mov/dta',
            '/home/chipdelmal/Documents/WorkSims/Mov/GA',
            '/home/chipdelmal/Documents/WorkSims/Mov/trp'
        )
    return (PT_DTA, PT_GA, PT_IMG)


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


def plotTraps(
    fig, ax, 
    trapsLocs, bestVal, sites, pTypes, radii, BQN,
    minX, minY, maxX, maxY,
    lw=.125, alpha=.5, sca=50
):
    (LW, ALPHA, SCA) = (lw, alpha, sca)
    (fig, ax) = plt.subplots(figsize=(15, 15))
    # Traps and sites ---------------------------------------------------------
    for trap in trapsLocs:
        plt.scatter(
            trap[0], trap[1], 
            marker="X", color='#f72585FA', s=250, zorder=25,
            edgecolors='w', linewidths=2
        )
        for r in radii:
            circle = plt.Circle(
                (trap[0], trap[1]), r, 
                color='#f7258509', fill=True, ls=':', lw=0, zorder=0
            )
            ax.add_patch(circle)
    for (i, site) in enumerate(sites):
        plt.scatter(
            site[0], site[1], 
            marker=MKRS[int(pTypes[i])], color=MCOL[int(pTypes[i])], 
            s=150, zorder=20, edgecolors='w', linewidths=2
        )
    # Traps network ----------------------------------------------------------- 
    (fig, ax) = plotNetwork(
        fig, ax, BQN*SCA, 
        np.asarray(trapsLocs), sites, 
        [0], c='#d81159', lw=LW*2, alpha=ALPHA*2
    )
    # Axes --------------------------------------------------------------------
    plt.tick_params(
        axis='both', which='both',
        bottom=False, top=False, left=False, right=False,
        labelbottom=False, labeltop=False, labelleft=False, labelright=False
    )
    ax.text(
        0.5, 0.5, '{:.2f}'.format(bestVal),
        horizontalalignment='center', verticalalignment='center',
        fontsize=100, color='#00000011',
        transform=ax.transAxes, zorder=5
    )
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(0)
    ax.set_aspect('equal')
    ax.set_xlim(minX-PAD, maxX+PAD)
    ax.set_ylim(minY-PAD, maxY+PAD)
    return (fig, ax)
