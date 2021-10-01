#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import MoNeT_MGDrivE as monet

STATES_NUM = 36
EPI_STATES = ('S', 'T', 'D', 'A', 'U', 'P', 'ICA', 'IB', 'ID', 'clin_inc')
epiLabels = monet.flatten_list(
    [[j+str(i) for i in range(STATES_NUM+1)] for j in EPI_STATES]
)
locus = (0, )
###############################################################################
# Ecology genotype counts
###############################################################################
HUM_DICT = OrderedDict((
    ('S', (('S', locus), )),
))
HUM_S = monet.geneFrequencies(HUM_DICT, epiLabels)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('H', locus), )),
    ('O-', (('W', locus), ('R', locus), ('B', locus)))
))
LDR_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('RB*', (('R', locus), ('B', locus) )),
    ('O-', (('H', locus), ('W', locus)))
))
LDR_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), ('B', locus), ('H', locus))),
    ('W-', (('W', locus), ))
))
LDR_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*LDR_ECO)
        yRange = popSize*2
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*LDR_HLT)
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*LDR_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*LDR_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'LDR')
