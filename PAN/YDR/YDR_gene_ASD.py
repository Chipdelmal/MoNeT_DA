

from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R
###############################################################################
genotypes = (
    'WWWW', 'WWWH', 'WWWR', 'WWWB', 'WWHH', 'WWHR', 'WWHB', 'WWRR', 'WWRB',
    'WWBB', 'WCWW', 'WCWH', 'WCWR', 'WCWB', 'WCHH', 'WCHR', 'WCHB', 'WCRR',
    'WCRB', 'WCBB', 'CCWW', 'CCWH', 'CCWR', 'CCWB', 'CCHH', 'CCHR', 'CCHB',
    'CCRR', 'CCRB', 'CCBB'
)
(locusA, locusB, locusF) = ((0, 1), (2, 3), (0, 1, 2, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('WA', (('W', locusA), )),
    ('WB', (('W', locusB), )),
    ('H',  (('H', locusF), )),
    ('C',  (('C', locusF), )),
    ('R',  (('R', locusF), )),
    ('B',  (('B', locusF), ))
))
ASD_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locusB), )),
    ('O-', (('W', locusB), ('R', locusB), ('B', locusB), ('C', locusB)))
))
ASD_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('C', locusA), )),
    ('O-', (('W', locusA), ('R', locusA), ('B', locusA), ('H', locusA)))
))
ASD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('H', locusA), ('R', locusA), ('B', locusA), ('C', locusA))),
    ('W-', (('W', locusA), ))
))
ASD_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=True)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*ASD_ECO)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*ASD_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*ASD_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*ASD_WLD)
        yRange = popSize
    return (aggD, yRange, 'autosomal')


