#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import numpy as np
import operator as op
from glob import glob
import matplotlib as mpl
from functools import reduce
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
mpl.rcParams['axes.linewidth'] = 1



def flatten(l):
    return reduce(lambda x, y: x+y, l)


def filterFromName(df, id, header):
    fltr = [True] * len(df)
    for ix in range(len(id)):
        fltr = fltr & (df[header[ix]] == id[ix])
    return fltr


def getXpId(pFile, idIx):
    splitXpId = re.split('_|-', pFile.split('/')[-1].split('.')[-2])
    xpId = [int(splitXpId[i]) for i in idIx]
    return xpId





def splitExpNames(PATH_OUT, ext='lzma'):
    out = [i.split('/')[-1].split('-')[0] for i in glob(PATH_OUT+'*.'+ext)]
    return sorted(list(set(out)))


def exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='', vLines=[0]):
    figArr = monet.plotNodeTraces(tS, STYLE)
    axTemp = figArr[0].get_axes()[0]
    axTemp.set_aspect(aspect=STYLE["aspect"])
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    axTemp.axes.xaxis.set_ticklabels([])
    axTemp.axes.yaxis.set_ticklabels([])
    axTemp.xaxis.set_tick_params(width=1)
    axTemp.yaxis.set_tick_params(width=1)
    axTemp.xaxis.set_ticks(np.arange(0, STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(0, STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.25, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.25, color=(0, 0, 0))
    axTemp.axvspan(vLines[0], vLines[1], alpha=0.2, facecolor='#3687ff', zorder=0)
    axTemp.tick_params(color=(0, 0, 0, 0.5))
    figArr[0].savefig(
            "{}/{}-{}.png".format(PATH_IMG, nS, append),
            dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='png',
            transparent=True, bbox_inches='tight', pad_inches=.05
        )
    plt.close('all')
    return True


def getExperimentsIDSets(PATH_EXP, skip=-1, ext='.lzma'):
    filesList = glob(PATH_EXP+'E*')
    fileNames = [i.split('/')[-1].split('.')[-2] for i in filesList]
    splitFilenames = [re.split('_|-', i)[:skip] for i in fileNames]
    ids = []
    for c in range(len(splitFilenames[0])):
        colSet = set([i[c] for i in splitFilenames])
        ids.append(sorted(list(colSet)))
    return ids


###############################################################################
# Response Surface
###############################################################################
def calcResponseSurface(
            iX, iY, dZ, scalers=(1, 1, 1),
            mthd='linear', NDX=1000, NDY=1000
        ):
    (xN, yN, zN) = (
            np.array([float(i/scalers[0]) for i in iX]),
            np.array([float(i/scalers[1]) for i in iY]),
            np.array([float(i/scalers[2]) for i in dZ])
        )
    (xRan, yRan, zRan) = (axisRange(i) for i in (xN, yN, zN))
    (xi, yi) = (
            np.linspace(xRan[0], xRan[1], NDX),
            np.linspace(yRan[0], yRan[1], NDY)
        )
    zi = griddata((xN, yN), zN, (xi[None, :], yi[:, None]), method=mthd)
    # Return variables
    ranges = (xRan, yRan, zRan)
    grid = (xN, yN, zN)
    surf = (xi, yi, zi)
    return {'ranges': ranges, 'grid': grid, 'surface': surf}


def axisRange(x):
    return (min(x), max(x))

###############################################################################
# Networks
###############################################################################

def calcNetworkDistance(G):
    nodesNum = len(G)
    for i in range(nodesNum):
        keys = G[i]
        for j in range(nodesNum):
            prb = keys.get(j)
            if prb is not None:
                weight = prb['weight']
                if weight > 0:
                    distance = 1 / prb['weight']
                else:
                    distance = np.Inf
                G[i][j]['distance'] = distance
    return G


def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    raise ValueError("'{char}' is not in list".format(char=char))

###############################################################################
# Save Figure
###############################################################################
def quickSave(fig, ax, path, name, dpi=750):
    fig.savefig(
        os.path.join(path, name),
        dpi=dpi, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format='png',
        transparent=True, bbox_inches='tight', pad_inches=0.01
    )


def quickSaveFig(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, bbox_inches='tight', pad_inches=.02
     )


def quickSaveFigPad(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, pad_inches=1
     )


# ############################################################################
# Code from:
#   http://ric70x7.github.io/20190121_buffers.html
# ############################################################################

import numpy as np
import geopandas as geop
from shapely import geometry
from shapely.ops import polygonize
from scipy.spatial import Voronoi
# from matplotlib import cm, colors, colorbar
from descartes import PolygonPatch
import matplotlib.pyplot as plt



def voronoi_polygons(X, margin=0):
    '''
    Returns a set of Voronoi polygons corresponding to a set of points X.
    Source: http://ric70x7.github.io/20190121_buffers.html

    :param X: Array of points (optional).
              Numpy array, shape = [n, 2].

    :param margin: Minimum margin to extend the outer polygons of the tessellation.
                   Non-negative float.

    :return: Geopandas data frame.
    '''
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
    '''
    Return a set of regular polygons around points X.
    Source: http://ric70x7.github.io/20190121_buffers.html

    :param X: Array of points (optional).
              Numpy array, shape = [n, 2].

    :param radius: Circumradius of the polygon.
                   Positive float.

    :param n_angles: Number of angles of each polygon.
                     Integer >= 3.

    :return: Geopandas data frame.
    '''
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
    '''
    Return a set of disjoint polygons around points X.
    Source: http://ric70x7.github.io/20190121_buffers.html

    :param X: Array of points (optional).
              Numpy array, shape = [n, 2].

    :param radius: Circumradius of the polygon.
                   Positive float.

    :param n_angles: Number of angles of each polygon.
                     Integer >= 3.

    :return: Geopandas data frame.
    '''
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
