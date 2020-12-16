

from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveY.R
###############################################################################
genotypes = (
    'XXWW','XXWG','XXWR','XXWB','XXGG','XXGR','XXGB','XXRR','XXRB','XXBB',
    'XYWW','XYWG','XYWR','XYWB','XYGG','XYGR','XYGB','XYRR','XYRB','XYBB',
    'XCWW','XCWG','XCWR','XCWB','XCGG','XCGR','XCGB','XCRR','XCRB','XCBB'
)
(locusA, locusB, locusF) = ((0, 1), (2, 3), (0, 1, 2, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('X', (('X', locusF), )),
    ('Y', (('Y', locusF), )),
    ('C', (('C', locusF), )),
    ('W', (('W', locusF), )),
    ('G', (('G', locusF), )),
    ('R', (('R', locusF), )),
    ('B', (('B', locusF), ))
))
YSD_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('G', locusB), )),
    ('O-', (('W', locusB), ('R', locusB), ('B', locusB))
    )
))
YSD_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('C', locusA), )),
    ('O-', (('X', locusA), ('Y', locusA)))   
))
YSD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('C', locusA), )),
    ('W-', (('X', locusA), ('Y', locusA)))
))
YSD_WLD = monet.carrierFrequencies(WLD_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*YSD_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*YSD_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*YSD_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*YSD_WLD)
        yRange = popSize
    return (aggD, yRange, 'yLinked')