
import tGD_aux as aux
import MoNeT_MGDrivE as monet
from collections import OrderedDict

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R
###############################################################################
genotypes = (
    'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
    'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
    'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
    'CCRR', 'CCRB', 'CCBB'
)
(locA, locB, locF) = ((0, 1), (2, 3), (0, 1, 2, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('R+B',   (('B', locB), ('R', locB))),
    ('W',     (('W', locB), )),
    ('H',     (('H', locB), )),
    ('Total', (
            ('H', locB), 
            ('W', locB), 
            ('R', locB), ('B', locB)
        )
    )
))
SDR_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Trash Plot genotype counts
###############################################################################
CAP_DICT = OrderedDict((
    ('W',     (('W', locA), )),
    ('C',     (('C', locA), )),
    ('Total', (
            ('C', locA), 
            ('W', locA)
        )
    )
))
# TGD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
SDR_CAP = monet.geneFrequencies(CAP_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locB), )),
    ('O-', (('W', locB), ('R', locB), ('B', locB)))
))
SDR_HLT = monet.geneFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*',  (('C', locA), )),
    ('W-',  (('W', locA), ))
))
# SDR_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
SDR_TRS = monet.geneFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('C', locA), )),
    ('W-', (('W', locA), ))
))
SDR_WLD = monet.carrierFrequencies(WLD_DICT, genotypes)

###############################################################################
# Custom genotype counts
###############################################################################
CST_DICT = OrderedDict((
    ('C*', (('C', locA), )),
    ('O-', (('W', locA), ))
))
SDR_CST = monet.carrierFrequencies(CST_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*SDR_ECO)
        yRange = popSize*2
    if TYPE == 'CAP':
        aggD = monet.generateAggregationDictionary(*SDR_CAP)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*SDR_HLT)
        yRange = popSize*2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*SDR_TRS)
        yRange = popSize*2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*SDR_WLD)
        yRange = popSize
    elif TYPE == 'CST':
        aggD = monet.generateAggregationDictionary(*SDR_CST)
        yRange = popSize/2
    return (aggD, yRange, 'splitDrive')