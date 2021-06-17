
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
FSR_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
FSR_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('R*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
FSR_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), )),
    ('W-', (('W', locus), ))
))
FSR_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*FSR_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*FSR_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*FSR_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*FSR_WLD)
        yRange = popSize
    return (aggD, yRange, 'fsRIDL')