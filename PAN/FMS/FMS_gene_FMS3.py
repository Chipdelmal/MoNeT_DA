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
genotypes = (
    "AABBCC", "aABBCC", "AAbBCC", "aAbBCC", "AABBcC", "aABBcC", "AAbBcC", "aAbBcC", 
    "aaBBCC", "aabBCC", "aaBBcC", "aabBcC", "AAbbCC", "aAbbCC", "AAbbcC", "aAbbcC", 
    "aabbCC", "aabbcC", "AABBcc", "aABBcc", "AAbBcc", "aAbBcc", "aaBBcc", "aabBcc", 
    "AAbbcc", "aAbbcc", "aabbcc"
)
(locA, locB, locC) = ((0, 1), (2, 3), (4, 5))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('A', (('A', locA), )), ('a', (('a', locA), )),
    ('B', (('B', locB), )), ('b', (('b', locB), )),
    ('C', (('C', locC), )), ('c', (('c', locC), ))
))
FMS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts (gRNA)
###############################################################################
HLT_DICT = OrderedDict((
    ('T*',   (('A', locA), ('B', locB), ('C', locC))),
    ('O-',   (('a', locA), ('b', locB), ('c', locC)))
))
FMS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)
FMS_HLT[1][0] = FMS_HLT[1][-1]
FMS_HLT[1][1] = FMS_HLT[1][-1]

###############################################################################
# Trash genotype counts (Cas9)
###############################################################################
TRS_DICT = OrderedDict((
    ('Cas9*',   (('A', locA), )),
    ('O-',      (('a', locA), ))
))
FMS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('A', locA), ('B', locB), ('C', locC))),
    ('W-', (('a', locA), ('b', locB), ('c', locC)))
))
FMS_WLD = monet.carrierFrequencies(WLD_DICT, genotypes, invert=False)

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'ECO':
        aggD = monet.generateAggregationDictionary(*FMS_ECO)
        yRange = popSize*4
    elif TYPE == 'HLT':
        aggD = monet.generateAggregationDictionary(*FMS_HLT)
        yRange = popSize
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*FMS_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*FMS_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'ifegenia_3')
