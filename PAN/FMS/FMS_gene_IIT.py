#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# Souce: https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-Wolbachia.R
#   W: Wolbachia
#   w: Wild
###############################################################################
genotypes = ('W', 'w')
locus = (0, )

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W', (('W', locus), )),
    ('w', (('w', locus), ))
))
IIT_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('W*', (('W', locus), )),
    ('w-', (('w', locus), ))
))
IIT_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('w*', (('w', locus), )),
    ('W-', (('W', locus), ))
))
IIT_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('w*', (('w', locus), )),
    ('W-', (('W', locus), ))
))
IIT_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*IIT_ECO)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*IIT_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*IIT_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*IIT_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'IIT')
