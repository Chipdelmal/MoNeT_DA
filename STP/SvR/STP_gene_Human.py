
import MoNeT_MGDrivE as monet

genotypes = ('S', 'I')
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Health genotype counts
###############################################################################
sGenes = (('S', allGeneIx), )
sPos = set(monet.aggregateGeneAppearances(genotypes, sGenes))
iGenes = (('I', allGeneIx), )
iPos = set(monet.aggregateGeneAppearances(genotypes, iGenes))
HUM_HLT= [list(i) for i in (iPos, sPos - iPos, sPos | iPos)]

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize=360000):
    if TYPE == 'HUM':
        aggD = monet.generateAggregationDictionary(
            ['I', 'S', 'Total'], HUM_HLT
        )
    yRange = popSize
    return (aggD, yRange, 'HUM')