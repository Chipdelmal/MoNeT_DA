
import tGD_aux as aux
import MoNeT_MGDrivE as monet
from collections import OrderedDict

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-tGD.R
###############################################################################
genotypes = (
    "WWWW", "PWWW", "MWWW", "RWWW", "BWWW", "WGWW", "PGWW", "MGWW", "RGWW",
    "BGWW", "WRWW", "PRWW", "MRWW", "RRWW", "BRWW", "WBWW", "PBWW", "MBWW",
    "RBWW", "BBWW", "PWPW", "MWPW", "PWRW", "BWPW", "PWWG", "PGPW", "MGPW",
    "PWRG", "BGPW", "PWWR", "PRPW", "MRPW", "PWRR", "BRPW", "PWWB", "PBPW",
    "MBPW", "PWRB", "BBPW", "MWMW", "MWRW", "BWMW", "MWWG", "MWPG", "MGMW",
    "MWRG", "BGMW", "MWWR", "MWPR", "MRMW", "MWRR", "BRMW", "MWWB", "MWPB",
    "MBMW", "MWRB", "BBMW", "RWRW", "BWRW", "RWWG", "PGRW", "MGRW", "RGRW",
    "BGRW", "RWWR", "PRRW", "MRRW", "RRRW", "BRRW", "RWWB", "PBRW", "MBRW",
    "RBRW", "BBRW", "BWBW", "BWWG", "BWPG", "BWMG", "BWRG", "BGBW", "BWWR",
    "BWPR", "BWMR", "BWRR", "BRBW", "BWWB", "BWPB", "BWMB", "BWRB", "BBBW",
    "WGWG", "PGWG", "MGWG", "RGWG", "BGWG", "WGWR", "PRWG", "MRWG", "RRWG",
    "BRWG", "WBWG", "PBWG", "MBWG", "RBWG", "BBWG", "PGPG", "MGPG", "PGRG",
    "BGPG", "PGWR", "PGPR", "MRPG", "PGRR", "BRPG", "PGWB", "PBPG", "MBPG",
    "PGRB", "BBPG", "MGMG", "MGRG", "BGMG", "MGWR", "MGPR", "MGMR", "MGRR",
    "BRMG", "MGWB", "MGPB", "MBMG", "MGRB", "BBMG", "RGRG", "BGRG", "RGWR",
    "PRRG", "MRRG", "RGRR", "BRRG", "RGWB", "PBRG", "MBRG", "RBRG", "BBRG",
    "BGBG", "BGWR", "BGPR", "BGMR", "BGRR", "BGBR", "BGWB", "BGPB", "BGMB",
    "BGRB", "BBBG", "WRWR", "PRWR", "MRWR", "RRWR", "BRWR", "WBWR", "PBWR",
    "MBWR", "RBWR", "BBWR", "PRPR", "MRPR", "PRRR", "BRPR", "PRWB", "PBPR",
    "MBPR", "PRRB", "BBPR", "MRMR", "MRRR", "BRMR", "MRWB", "MRPB", "MBMR",
    "MRRB", "BBMR", "RRRR", "BRRR", "RRWB", "PBRR", "MBRR", "RBRR", "BBRR",
    "BRBR", "BRWB", "BRPB", "BRMB", "BRRB", "BBBR", "WBWB", "PBWB", "MBWB",
    "RBWB", "BBWB", "PBPB", "MBPB", "PBRB", "BBPB", "MBMB", "MBRB", "BBMB",
    "RBRB", "BBRB", "BBBB"
)
(locA, locB) = ((0, 2), (1, 3))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W',   (('W', locB), )),
    ('R+B', (('R', locB), ('B', locB))),
    ('G',   (('G', locB), )),
    ('Total', (
            ('W', locB), 
            ('R', locB), 
            ('B', locB),
            ('G', locB)
        )
    )
))
TGD_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Trash Plot genotype counts
###############################################################################
CAP_DICT = OrderedDict((
    ('W', (('W', locA), )),
    ('C', (('P', locA), ('M', locA))),
    ('R+B', (('R', locA), ('B', locA))),
    ('Total', (
            ('W', locA), 
            ('P', locA), ('M', locA),
            ('R', locA), ('B', locA)
        )
    )
))
# TGD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
TGD_CAP = monet.geneFrequencies(CAP_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('G*', (('G', locB), )),
    ('O-', (('W', locB), ('R', locB), ('B', locB)))
))
TGD_HLT = monet.geneFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('C*', (('P', locA), ('M', locA))),
    ('O-', (('W', locA), ('R', locA), ('B', locA)))
))
# TGD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
TGD_TRS = monet.geneFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('P', locA),('M', locA), ('R', locA), ('B', locA) )),
    ('W-', (('W', locA), ))
))
TGD_WLD = monet.carrierFrequencies(WLD_DICT, genotypes)

###############################################################################
# Custom genotype counts
###############################################################################
CST_DICT = OrderedDict((
    ('C*', (('P', locA), ('M', locA))),
    ('O-', (('W', locA), ('R', locA), ('B', locA)))
))
TGD_CST = monet.carrierFrequencies(CST_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*TGD_ECO)
        yRange = popSize*2
    if TYPE == 'CAP':
        aggD = monet.generateAggregationDictionary(*TGD_CAP)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*TGD_HLT)
        yRange = popSize*2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*TGD_TRS)
        yRange = popSize*2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*TGD_WLD)
        yRange = popSize
    elif TYPE == 'CST':
        aggD = monet.generateAggregationDictionary(*TGD_CST)
        yRange = popSize/2
    return (aggD, yRange, 'tGD')
