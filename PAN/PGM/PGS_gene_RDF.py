#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# Souce: https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-RIDL.R
#   W: Wild-type allele
#   R: OX513 RIDL allele
###############################################################################
genotypes = ('WW', 'WR', 'RR')
locus = (0, 1)

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('W', (('W', locus), )),
    ('R', (('R', locus), ))
))
RDF_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts
###############################################################################
HLT_DICT = OrderedDict((
    ('H*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
RDF_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts
###############################################################################
TRS_DICT = OrderedDict((
    ('R*', (('R', locus), )),
    ('O-', (('W', locus), ))
))
RDF_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('R', locus), )),
    ('W-', (('W', locus), ))
))
RDF_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*RDF_ECO)
        yRange = popSize*4
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*RDF_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*RDF_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*RDF_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'fsRIDL')
