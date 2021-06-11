
from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ASmidler.R
###############################################################################

genotypes = (
    'WWWW','PWWW','MWWW','WGWW','PGWW','MGWW','WRWW','PRWW','MRWW','WBWW','PBWW',
    'MBWW','MWPW','PWWG','MGPW','PWWR','MRPW','PWWB','MBPW','MWWG','MWPG','MWWR',
    'MWPR','MWWB','MWPB','WGWG','PGWG','MGWG','WGWR','PRWG','MRWG','WBWG','PBWG',
    'MBWG','MGPG','PGWR','MRPG','PGWB','MBPG','MGWR','MGPR','MGWB','MGPB','WRWR',
    'PRWR','MRWR','WBWR','PBWR','MBWR','MRPR','PRWB','MBPR','MRWB','MRPB','WBWB',
    'PBWB','MBWB','MBPB'
)
(locusA, locusB, locusF) = ((0, 2), (1, 3), (0, 1, 2, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('WA',  (('W', locusA), )),
    ('P',   (('P', locusA), )),
    ('M',   (('M', locusA), )),
    ('WB',  (('W', locusB), )),
    ('G',   (('G', locusB), )),
    ('B',   (('B', locusB), )),
    ('R',   (('R', locusB), ))
))
CRS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('G', locusB), )),
    ('O-', (('W', locusB), ('B', locusB), ('R', locusB)))
))
CRS_HLT = monet.geneFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('P', locusA), ('M', locusA))),
    ('O-', (('W', locusA), ))
))
CRS_TRS = monet.geneFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('B', locusB), ('R', locusB), ('G', locusB))),
    ('W-', (('W', locusB), ))
))
CRS_WLD = monet.geneFrequencies(WLD_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*CRS_ECO)
        yRange = popSize
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*CRS_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*CRS_TRS)
        yRange = popSize
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*CRS_WLD)
        yRange = popSize
    return (aggD, yRange, 'SplitDrive-DsX')
