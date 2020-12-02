
import MoNeT_MGDrivE as monet

genotypes = (
    'WWXX','WAXX','WBXX','AAXX','ABXX','BBXX','WWXR','WAXR','WBXR',
    'AAXR','ABXR','BBXR','WWRR','WARR','WBRR','AARR','ABRR','BBRR',
    'WWXY','WAXY','WBXY','AAXY','ABXY','BBXY','WWRY','WARY','WBRY',
    'AARY','ABRY','BBRY'
)
allGeneIx = list(range(len(genotypes[0])))


###############################################################################
# Ecology genotype counts
###############################################################################
aGenes = (('A', allGeneIx), )
aPos = monet.aggregateGeneAppearances(genotypes, aGenes)
xGenes = (('X', allGeneIx), )
xPos = monet.aggregateGeneAppearances(genotypes, xGenes)
yGenes = (('Y', allGeneIx), )
yPos = monet.aggregateGeneAppearances(genotypes, yGenes)
cGenes = (('C', allGeneIx), )
cPos = monet.aggregateGeneAppearances(genotypes, cGenes)
wGenes = (('W', allGeneIx), )
wPos = monet.aggregateGeneAppearances(genotypes, wGenes)
gGenes = (('G', allGeneIx), )
gPos = monet.aggregateGeneAppearances(genotypes, gGenes)
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
YSD_ECO = (aPos, xPos, yPos, cPos, wPos, gPos, rPos, bPos)

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
YSD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

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
YSD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

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
YSD_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(
            ['A', 'X', 'Y', 'C', 'W', 'G', 'R', 'B'], YSD_ECO
        )
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], YSD_HLT
        )
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], YSD_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], YSD_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'autosomal')
