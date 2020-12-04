
import MoNeT_MGDrivE as monet

genotypes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
wGenes = (('W', allGeneIx), )
wPos = monet.aggregateGeneAppearances(genotypes, wGenes)
hGenes = (('H', allGeneIx), )
hPos = monet.aggregateGeneAppearances(genotypes, hGenes)
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
LDR_ECO = (wPos, hPos, rPos, bPos)
###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('H', allGeneIx), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
oGenes = (('W', allGeneIx), ('R', allGeneIx), ('B', allGeneIx))
oPos = set(monet.aggregateGeneAppearances(genotypes, oGenes))
LDR_HLT = [list(i) for i in (hPos, oPos - hPos, oPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
rGenes = (('R', allGeneIx), ('B', allGeneIx))
rPos = set(monet.aggregateGeneAppearances(genotypes, rGenes))
oGenes = (('W', allGeneIx), ('H', allGeneIx))
oPos = set(monet.aggregateGeneAppearances(genotypes, oGenes))
LDR_TRS = [list(i) for i in (hPos, oPos - rPos, oPos | rPos)]

###############################################################################
# Wild genotype counts
###############################################################################
wGenes = (('W', allGeneIx), )
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
oGenes = (('H', allGeneIx), ('R', allGeneIx), ('B', allGeneIx))
oPos = set(monet.aggregateGeneAppearances(genotypes, oGenes))
LDR_WLD = [list(i) for i in (wPos, oPos - wPos, oPos | wPos)]

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(
            ['W', 'H', 'R', 'B'], LDR_ECO
        )
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(
            ['H*', 'O-', 'Total'], LDR_HLT
        )
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(
            ['R*', 'O-', 'Total'], LDR_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], LDR_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'LDR')