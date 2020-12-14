
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_main.R
###############################################################################

import MoNeT_MGDrivE as monet

genotypes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locus = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
wGenes = (('W', locus), )
hGenes = (('H', locus), )
rGenes = (('R', locus), )
bGenes = (('B', locus), )
genesSlot = (wGenes, hGenes, rGenes, bGenes)
LDR_ECO = [monet.aggregateGeneAppearances(genotypes, i) for i in genesSlot]
###############################################################################
# Health genotype counts
###############################################################################
hGenes = (('H', locus), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
oGenes = (('W', locus), ('R', locus), ('B', locus))
oPos = set(monet.aggregateGeneAppearances(genotypes, oGenes))
LDR_HLT = [list(i) for i in (hPos, oPos - hPos, oPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
rGenes = (('R', locus), ('B', locus))
rPos = set(monet.aggregateGeneAppearances(genotypes, rGenes))
oGenes = (('W', locus), ('H', locus))
oPos = set(monet.aggregateGeneAppearances(genotypes, oGenes))
LDR_TRS = [list(i) for i in (hPos, oPos - rPos, oPos | rPos)]

###############################################################################
# Wild genotype counts
###############################################################################
wGenes = (('W', locus), )
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
oGenes = (('H', locus), ('R', locus), ('B', locus))
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
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], LDR_WLD
        )
        yRange = popSize/2
    return (aggD, yRange, 'LDR')