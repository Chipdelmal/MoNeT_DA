
from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-RIDL.R
###############################################################################
genotypes = ('WW', 'Ww', 'ww')
locus = (0, 1)

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('A', (('W', locus), )),
    ('a', (('w', locus), ))
))
SIT_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('W', locus), )),
    ('O-', (('w', locus), ))
))
SIT_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('H*', (('W', locus), )),
    ('O-', (('w', locus), ))
))
SIT_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('W', locus), )),
    ('W-', (('w', locus), ))
))
SIT_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*SIT_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*SIT_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*SIT_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*SIT_WLD)
        yRange = popSize
    return (aggD, yRange, 'SIT')