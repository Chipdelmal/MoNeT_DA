

from collections import OrderedDict
import MoNeT_MGDrivE as monet


###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-CRISPR2MF.R
###############################################################################

genotypes = (
    'WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB'
)
(locusF, ) = ((0, 1), )

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W',   (('W', locusF), )),
    ('H',   (('H', locusF), )),
    ('B',   (('B', locusF), )),
    ('R',   (('R', locusF), ))
))
CRS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locusF), )),
    ('O-', (('W', locusF), ('B', locusF), ('R', locusF)))
))
CRS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('H', locusF), )),
    ('O-', (('W', locusF), ('B', locusF), ('R', locusF)))
))
CRS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('B', locusF), ('R', locusF), ('H', locusF))),
    ('W-', (('W', locusF), ))
))
CRS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*CRS_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*CRS_HLT)
        yRange = popSize/4
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*CRS_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*CRS_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'CRISPR')