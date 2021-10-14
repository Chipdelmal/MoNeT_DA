
import numpy as np

###############################################################################
# Initialization
###############################################################################
def initChromosome(trapsNum, xRan, yRan):
    xCoords = np.random.uniform(xRan[0], xRan[1], trapsNum)
    yCoords = np.random.uniform(yRan[0], yRan[1], trapsNum)
    chromosome = [val for pair in zip(xCoords, yCoords) for val in pair]
    return chromosome