
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderY.R
###############################################################################

import MoNeT_MGDrivE as monet

genotypes = (
    'XX','XR','RR','XY','XA','XB','RY','RA','RB'
)
allGeneIx = list(range(len(genotypes[0])))


###############################################################################
# Ecology genotype counts
###############################################################################
xGenes = (('X', allGeneIx), )
yGenes = (('Y', allGeneIx), )
aGenes = (('A', allGeneIx), )
bGenes = (('B', allGeneIx), )
rGenes = (('R', allGeneIx), )
genes = (xGenes, yGenes, aGenes, bGenes, rGenes)
YXS_ECO = [monet.aggregateGeneAppearances(genotypes, i) for i in genes]
YXS_ECO_L = ('X', 'Y', 'A', 'B', 'R')

###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('A', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('Y', (0, 1)), 
    ('R', (0, 1)), ('B', (0, 1))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YXS_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
hGenes = (('R', (0, 1)), ('B', (0, 1)))
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('Y', (0, 1)),
    ('A', (0, 1))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YXS_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('Y', (0, 1)), ('X', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('A', (0, 1)), ('R', (0, 1)), ('B', (0, 1))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YXS_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(YXS_ECO_L, YXS_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], YXS_HLT
        )
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(
            ['C*', 'O-', 'Total'], YXS_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], YXS_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'yLinked')