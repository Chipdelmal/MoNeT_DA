
import MoNeT_MGDrivE as monet

genotypes = (
    'XX','XR','RR','XY','XA','XB','RY','RA','RB'
)
allGeneIx = list(range(len(genotypes[0])))


###############################################################################
# Ecology genotype counts
###############################################################################
xGenes = (('X', allGeneIx), )
xPos = monet.aggregateGeneAppearances(genotypes, xGenes)
yGenes = (('Y', allGeneIx), )
yPos = monet.aggregateGeneAppearances(genotypes, yGenes)
aGenes = (('A', allGeneIx), )
aPos = monet.aggregateGeneAppearances(genotypes, aGenes)
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
YXS_ECO = (xPos, yPos, aPos, bPos, rPos)

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
YXS_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

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
YXS_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('Y', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', (0, 1)), ('C', (0, 1)),
    ('G', (2, 3)), ('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3))
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YXS_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(
            ['X', 'Y', 'A', 'B', 'R'], YXS_ECO
        )
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