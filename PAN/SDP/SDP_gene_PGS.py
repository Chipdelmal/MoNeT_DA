
from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-RIDL.R
###############################################################################
genotypes = ('WW', 'WR', 'RR')
locus = (0, 1)

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W', (('W', locus), )),
    ('R', (('R', locus), ))
))
PGS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
PGS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('H*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
PGS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), )),
    ('W-', (('W', locus), ))
))
PGS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*PGS_ECO)
        yRange = popSize/2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*PGS_HLT)
        yRange = popSize/4
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*PGS_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*PGS_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'Theoretical')