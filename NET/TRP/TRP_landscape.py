
import math
import numpy as np
import numpy.random as rand
import MoNeT_MGDrivE as monet


POINTS = 10
(xRan, yRan) = ((-10, 10), (-10, 10))
# Generate pointset -----------------------------------------------------------
coords = list(zip(
    rand.uniform(*xRan, POINTS), 
    rand.uniform(*yRan, POINTS)
))
# Generate matrices -----------------------------------------------------------
dist = monet.calculateDistanceMatrix(coords)
tau = monet.zeroInflatedExponentialMigrationKernel(
    dist, 
    [0.2, 1.0e-10, math.inf],
    zeroInflation=0.75
)
tau[0]