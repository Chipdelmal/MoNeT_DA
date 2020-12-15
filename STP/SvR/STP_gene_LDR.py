
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
oGenes = (('W', locus), ('R', locus), ('B', locus))
genesSlot = (hGenes, oGenes)
(hPos, oPos) = [set(monet.aggregateGeneAppearances(genotypes, i)) for i in genesSlot]
LDR_HLT = [list(i) for i in (hPos, oPos - hPos, oPos | hPos)]

###############################################################################
# Trash genotype counts
###############################################################################
rGenes = (('R', locus), ('B', locus))
oGenes = (('W', locus), ('H', locus))
genesSlot = (rGenes, oGenes)
(rPos, oPos) = [set(monet.aggregateGeneAppearances(genotypes, i)) for i in genesSlot]
LDR_TRS = [list(i) for i in (rPos, oPos - rPos, oPos | rPos)]

###############################################################################
# Wild genotype counts
###############################################################################
wGenes = (('W', locus), )
oGenes = (('H', locus), ('R', locus), ('B', locus))
(wPos, oPos) = [set(monet.aggregateGeneAppearances(genotypes, i)) for i in genesSlot]
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