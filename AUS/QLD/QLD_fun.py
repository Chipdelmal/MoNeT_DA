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
