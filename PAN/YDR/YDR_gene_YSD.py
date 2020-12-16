

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
YSD_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

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
YSD_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
hGenes = (('C', locusA), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', locusA), ('Y', locusA),
    ('G', locusB), ('W', locusB), ('R', locusB), ('B', locusB)
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YSD_TRS = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]

###############################################################################
# Wild genotype counts
###############################################################################
hGenes = (('Y', locusA), )
hPos = set(monet.aggregateGeneAppearances(genotypes, hGenes))
wGenes = (
    ('X', locusA), ('C', locusA),
    ('G', locusB), ('W', locusB), ('R', locusB), ('B', locusB)
)
wPos = set(monet.aggregateGeneAppearances(genotypes, wGenes))
YSD_WLD = [list(i) for i in (hPos, wPos - hPos, wPos | hPos)]


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
        aggD = monet.generateAggregationDictionary(
            ['C*', 'O-', 'Total'], YSD_TRS
        )
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(
            ['O-', 'W*', 'Total'], YSD_WLD
        )
        yRange = popSize
    return (aggD, yRange, 'yLinked')