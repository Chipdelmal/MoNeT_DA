

from collections import OrderedDict
import MoNeT_MGDrivE as monet
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/
###############################################################################

genotypes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locus = (0, 1)

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W', (('W', locus), )),
    ('H', (('H', locus), )),
    ('R', (('R', locus), )),
    ('B', (('B', locus), ))
))
SIT_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locus), )),
    ('O-', (('W', locus), ('R', locus), ('B', locus)))
))
SIT_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('RB*', (('R', locus), ('B', locus) )),
    ('O-', (('H', locus), ('W', locus)))
))
SIT_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), ('B', locus), ('H', locus))),
    ('W-', (('W', locus), ))
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
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*SIT_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*SIT_WLD)
        yRange = popSize
    return (aggD, yRange, 'SIT')