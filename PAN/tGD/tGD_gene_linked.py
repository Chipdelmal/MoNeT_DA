
import tGD_aux as aux
import MoNeT_MGDrivE as monet
from collections import OrderedDict

###############################################################################
# https://github.com/Chipdelmal/MGDrivE/blob/fb2106b7cfd52116121c8b6a4fa14ad360056e40/MGDrivE/R/Cube-CRISPR2MF.R
###############################################################################
genotypes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locus = (0, 1)

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W',     (('W', locus), )),
    ('H',     (('H', locus), )),
    ('R+B',   (('R', locus), ('B', locus))),
    ('Total', (
        ('W', locus), 
        ('H', locus), 
        ('R', locus), ('B', locus))
    )
))
LDR_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Trash Plot genotype counts
###############################################################################
CAP_DICT = OrderedDict((
    ('W',     (('W', locus), )),
    ('H',     (('H', locus), )),
    ('R+B',   (('R', locus), ('B', locus))),
    ('Total', (
        ('W', locus), 
        ('H', locus), 
        ('R', locus), ('B', locus))
    )
))
# TGD_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
LDR_CAP = monet.geneFrequencies(CAP_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locus), )),
    ('O-', (('W', locus), ('R', locus), ('B', locus))),
    ('T',  (('H', locus), ('W', locus), ('R', locus), ('B', locus)))
))
LDR_HLT = monet.geneFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('RB*', (('R', locus), ('B', locus) )),
    ('O-', (('H', locus), ('W', locus)))
))
# LDR_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)
LDR_TRS = monet.geneFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), ('B', locus), ('H', locus))),
    ('W-', (('W', locus), ))
))
LDR_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Cas9 genotype counts
###############################################################################
CST_DICT = OrderedDict((
    ('H*', (('H', locus), )),
    ('O-', (('W', locus), ('R', locus), ('B', locus)))
))
LDR_CST = monet.carrierFrequencies(CST_DICT, genotypes)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*LDR_ECO)
        yRange = popSize*2
    if TYPE == 'CAP':
        aggD = monet.generateAggregationDictionary(*LDR_ECO)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*LDR_HLT)
        yRange = popSize*4
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*LDR_TRS)
        yRange = popSize*2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*LDR_WLD)
        yRange = popSize
    elif TYPE == 'CST':
        aggD = monet.generateAggregationDictionary(*LDR_CST)
        yRange = popSize/2
    return (aggD, yRange, 'linkedDrive')
