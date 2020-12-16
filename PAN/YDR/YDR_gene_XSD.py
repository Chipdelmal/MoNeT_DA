
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveX.R
###############################################################################

import MoNeT_MGDrivE as monet

genotypes = (
    'XXWW','XXWG','XXWR','XXWB','XXGG','XXGR','XXGB','XXRR','XXRB','XXBB',
    'XCWW','XCWG','XCWR','XCWB','XCGG','XCGR','XCGB','XCRR','XCRB','XCBB',
    'CCWW','CCWG','CCWR','CCWB','CCGG','CCGR','CCGB','CCRR','CCRB','CCBB',
    'XYWW','XYWG','XYWR','XYWB','XYGG','XYGR','XYGB','XYRR','XYRB','XYBB',
    'CYWW','CYWG','CYWR','CYWB','CYGG','CYGR','CYGB','CYRR','CYRB','CYBB'
)
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
xGenes = (('X', allGeneIx), )
yGenes = (('Y', allGeneIx), )
cGenes = (('C', allGeneIx), )
wGenes = (('W', allGeneIx), )
gGenes = (('G', allGeneIx), )
rGenes = (('R', allGeneIx), )
bGenes = (('B', allGeneIx), )
genes = (xGenes, yGenes, cGenes, wGenes, gGenes, rGenes, bGenes)
XSD_ECO = [monet.aggregateGeneAppearances(genotypes, i) for i in genes]
XSD_ECO_L = ('X', 'Y', 'C', 'W', 'G', 'R', 'B')

###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('G', (2, 3)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('Y', (0, 1)), ('C', (0, 1)), 
    ('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
XSD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
hGenes = (('C', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('Y', (0, 1)),
    ('G', (2, 3)), ('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
XSD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('X', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('C', (0, 1)),
    ('G', (2, 3)), ('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
XSD_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(XSD_ECO_L, XSD_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], XSD_HLT
        )
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(
            ['C*', 'O-', 'Total'], XSD_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], XSD_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'xLinked')