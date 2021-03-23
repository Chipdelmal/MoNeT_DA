
from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderMF.R
###############################################################################
genotypes = (
    'WWXX','WAXX','WBXX','AAXX','ABXX','BBXX','WWXR','WAXR','WBXR',
    'AAXR','ABXR','BBXR','WWRR','WARR','WBRR','AARR','ABRR','BBRR',
    'WWXY','WAXY','WBXY','AAXY','ABXY','BBXY','WWRY','WARY','WBRY',
    'AARY','ABRY','BBRY'
)
(locusA, locusB, locusF) = ((0, 1), (2, 3), (0, 1, 2, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('A', (('A', locusF), )),
    ('X', (('X', locusF), )),
    ('Y', (('Y', locusF), )),
    ('W', (('W', locusF), )),
    ('R', (('R', locusF), )),
    ('B', (('B', locusF), ))
))
AXS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('A', locusA), )),
    ('O-', (
            ('W', locusA), ('X', locusA), ('Y', locusA),
            ('R', locusA), ('B', locusA)
        )
    )
))
AXS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT =  OrderedDict((
    ('A*', (('A', locusA), )),
    ('O-', (
            ('W', locusA), ('X', locusA), ('Y', locusA),
            ('R', locusA), ('B', locusA)
        )
    )
))
AXS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (
            ('A', locusA), ('X', locusA), ('Y', locusA),
            ('R', locusA), ('B', locusA)
        )
    ),
    ('W-', (('W', locusA), ))
))
AXS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*AXS_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*AXS_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*AXS_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*AXS_WLD)
        yRange = popSize
    return (aggD, yRange, 'autosomal')
