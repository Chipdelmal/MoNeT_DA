
from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveX.R
###############################################################################
genotypes = (
    'XXWW','XXWG','XXWR','XXWB','XXGG','XXGR','XXGB','XXRR','XXRB','XXBB',
    'XCWW','XCWG','XCWR','XCWB','XCGG','XCGR','XCGB','XCRR','XCRB','XCBB',
    'CCWW','CCWG','CCWR','CCWB','CCGG','CCGR','CCGB','CCRR','CCRB','CCBB',
    'XYWW','XYWG','XYWR','XYWB','XYGG','XYGR','XYGB','XYRR','XYRB','XYBB',
    'CYWW','CYWG','CYWR','CYWB','CYGG','CYGR','CYGB','CYRR','CYRB','CYBB'
)
(locusA, locusB, locusF) = ((0, 1), (2, 3), list(range(len(genotypes[0]))))

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
XSD_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('G', locusB), )),
    ('O-', (
            ('X', locusA), ('Y', locusA), ('C', locusA), 
            ('W', locusB), ('R', locusB), ('B', locusB)
        )
    )
))
XSD_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('C', locusA), )),
    ('O-', (
            ('X', locusA), ('Y', locusA), 
            ('G', locusB), ('W', locusB), ('R', locusB), ('B', locusB)
        )
    )
))
XSD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('C', locusA), )),
    ('W-', (('X', locusA), ('Y', locusA)))
))
XSD_WLD= monet.carrierFrequencies(WLD_DICT, genotypes, invert=True)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*XSD_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*XSD_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*XSD_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*XSD_WLD)
        yRange = popSize
    return (aggD, yRange, 'xLinked')