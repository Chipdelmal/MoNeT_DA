
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderMF.R
###############################################################################

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
xGenes = (('X', allGeneIx), )
yGenes = (('Y', allGeneIx), )
wGenes = (('W', allGeneIx), )
rGenes = (('R', allGeneIx), )
bGenes = (('B', allGeneIx), )
genes = (aGenes, xGenes, yGenes, wGenes, rGenes, bGenes)
YSD_ECO = [monet.aggregateGeneAppearances(genotypes, i) for i in genes]
YSD_ECO_L = ('A', 'X', 'Y', 'W', 'R', 'B')

###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('A', allGeneIx), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('W', allGeneIx), ('X', allGeneIx), ('Y', allGeneIx),
    ('R', allGeneIx), ('B', allGeneIx)
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YSD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
hGenes = (('R', allGeneIx), ('B', allGeneIx))
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('W', allGeneIx), ('X', allGeneIx), ('Y', allGeneIx),
    ('A', allGeneIx)
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YSD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('W', allGeneIx), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('A', allGeneIx), ('X', allGeneIx), ('Y', allGeneIx),
    ('R', allGeneIx), ('B', allGeneIx)
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YSD_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(YSD_ECO_L, YSD_ECO)
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
