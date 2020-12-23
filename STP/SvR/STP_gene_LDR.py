

from collections import OrderedDict
import MoNeT_MGDrivE as monet
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_main.R
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
LDR_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locus), )),
    ('O-', (('W', locus), ('R', locus), ('B', locus)))
))
LDR_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('RB*', (('R', locus), ('B', locus) )),
    ('O-', (('H', locus), ('W', locus)))
))
LDR_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), ('B', locus), ('H', locus))),
    ('W-', (('W', locus), ))
))
LDR_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*LDR_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*LDR_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*LDR_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*LDR_WLD)
        yRange = popSize
    return (aggD, yRange, 'LDR')