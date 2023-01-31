#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import MoNeT_MGDrivE as monet

###############################################################################
# Souce: https://github.com/Chipdelmal/MGDrivE/blob/master/Main/pgSIT_Femaless/cubePgSIT.R
#   A/a: Cas locus, 
#   B/b: gRNA locus, 
#   C/c: female viability target site 1
#   D/d: female viability target site 2
#   E/e: female viability target site 3
#   ...
#   X/x: male fertility target site
###############################################################################
genotypes = ("WW", "WR", "RR")
(locA, locB, locC, locD) = ((0, 1), (2, 3), (4, 5), (6, 7))
###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('T*',   (('W', locA), ('R', locA))),
    ('O-',   (('W', locA), ('R', locA)))
))
PGS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts (gRNA)
###############################################################################
HLT_DICT = OrderedDict((
    ('T*',   (('W', locA), ('R', locA))),
    ('O-',   (('W', locA), ('R', locA)))
))
PGS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)
PGS_HLT = [PGS_HLT[0], [PGS_HLT[1][0], PGS_HLT[1][-1], PGS_HLT[1][-1]]]

###############################################################################
# Trash genotype counts (Cas9)
###############################################################################
TRS_DICT = OrderedDict((
    ('T*',   (('W', locA), ('R', locA))),
    ('O-',   (('W', locA), ('R', locA)))
))
PGS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('T*',   (('W', locA), ('R', locA))),
    ('O-',   (('W', locA), ('R', locA)))
))
PGS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*PGS_ECO)
        yRange = popSize*4
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*PGS_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*PGS_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*PGS_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'pgSIT')
