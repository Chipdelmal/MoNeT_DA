
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R
###############################################################################

import MoNeT_MGDrivE as monet

genotypes = (
    'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
    'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
    'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
    'CCRR', 'CCRB', 'CCBB'
)
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
wAGenes = (('W', (0, 1)), )
wAPos = monet.aggregateGeneAppearances(genotypes, wAGenes)
hGenes = (('H', allGeneIx), )
hPos = monet.aggregateGeneAppearances(genotypes, hGenes)
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
cGenes = (('C', allGeneIx), )
cPos = monet.aggregateGeneAppearances(genotypes, cGenes)
wBGenes = (('W', (2, 3)), )
wBPos = monet.aggregateGeneAppearances(genotypes, wBGenes)
ASD_ECO = (wAPos, hPos, rPos, bPos, cPos, wBPos)

###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('H', (2, 3)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (('W', (2, 3)), ('R', (2, 3)), ('B', (2, 3)), ('C', (2, 3)))
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
ASD_HLT = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
hGenes = (('C', (0, 1)), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (('W', (0, 1)), ('R', (0, 1)), ('B', (0, 1)), ('H', (0, 1)))
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
ASD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('H', (0, 1)), ('R', (0, 1)), ('B', (0, 1)), ('C', (0, 1)))
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (('W', (0, 1)), )
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
ASD_WLD = [list(i) for i in (hPos - wPos, wPos, wPos | hPos)]


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(
            ['WA', 'H', 'R', 'B', 'C', 'WB'], ASD_ECO
        )
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], ASD_HLT
        )
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(
            ['C*', 'O-', 'Total'], ASD_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], ASD_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'autosomal')


