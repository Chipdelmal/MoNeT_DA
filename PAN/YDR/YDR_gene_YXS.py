

from collections import OrderedDict
import MoNeT_MGDrivE as monet
###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderY.R
###############################################################################
genotypes = (
    'XX','XR','RR','XY','XA','XB','RY','RA','RB'
)
(locusA, locusF) = ((0, 1), (0, 1))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('X', (('X', locusF), )),
    ('Y', (('Y', locusF), )),
    ('A', (('A', locusF), )),
    ('B', (('B', locusF), )),
    ('R', (('R', locusF), ))
))
YXS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('A', locusA), )),
    ('O-', (
            ('X', locusA), ('Y', locusA),
            ('R', locusA), ('B', locusA)
        )
    )
))
YXS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('H*', (('A', locusA), )),
    ('O-', (
            ('X', locusA), ('Y', locusA),
            ('R', locusA), ('B', locusA)
        )
    )
))
YXS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('A', locusA), ('R', locusA), ('B', locusA))),
    ('W-', (
            ('X', locusA), ('Y', locusA)
        )
    )
))
YXS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=True)


###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*YXS_ECO)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*YXS_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*YXS_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*YXS_WLD)
        yRange = popSize
    return (aggD, yRange, 'yLinked')