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
    "AABBCCDDEE", "aABBCCDDEE", "AAbBCCDDEE", "aAbBCCDDEE", "AABBcCDDEE", "aABBcCDDEE", 
    "AAbBcCDDEE", "aAbBcCDDEE", "AABBCCdDEE", "aABBCCdDEE", "AAbBCCdDEE", "aAbBCCdDEE", 
    "AABBcCdDEE", "aABBcCdDEE", "AAbBcCdDEE", "aAbBcCdDEE", "AABBCCDDeE", "aABBCCDDeE", 
    "AAbBCCDDeE", "aAbBCCDDeE", "AABBcCDDeE", "aABBcCDDeE", "AAbBcCDDeE", "aAbBcCDDeE", 
    "AABBCCdDeE", "aABBCCdDeE", "AAbBCCdDeE", "aAbBCCdDeE", "AABBcCdDeE", "aABBcCdDeE", 
    "AAbBcCdDeE", "aAbBcCdDeE", "aaBBCCDDEE", "aabBCCDDEE", "aaBBcCDDEE", "aabBcCDDEE", 
    "aaBBCCdDEE", "aabBCCdDEE", "aaBBcCdDEE", "aabBcCdDEE", "aaBBCCDDeE", "aabBCCDDeE", 
    "aaBBcCDDeE", "aabBcCDDeE", "aaBBCCdDeE", "aabBCCdDeE", "aaBBcCdDeE", "aabBcCdDeE", 
    "AAbbCCDDEE", "aAbbCCDDEE", "AAbbcCDDEE", "aAbbcCDDEE", "AAbbCCdDEE", "aAbbCCdDEE", 
    "AAbbcCdDEE", "aAbbcCdDEE", "AAbbCCDDeE", "aAbbCCDDeE", "AAbbcCDDeE", "aAbbcCDDeE", 
    "AAbbCCdDeE", "aAbbCCdDeE", "AAbbcCdDeE", "aAbbcCdDeE", "aabbCCDDEE", "aabbcCDDEE", 
    "aabbCCdDEE", "aabbcCdDEE", "aabbCCDDeE", "aabbcCDDeE", "aabbCCdDeE", "aabbcCdDeE", 
    "AABBccDDEE", "aABBccDDEE", "AAbBccDDEE", "aAbBccDDEE", "AABBccdDEE", "aABBccdDEE", 
    "AAbBccdDEE", "aAbBccdDEE", "AABBccDDeE", "aABBccDDeE", "AAbBccDDeE", "aAbBccDDeE", 
    "AABBccdDeE", "aABBccdDeE", "AAbBccdDeE", "aAbBccdDeE", "aaBBccDDEE", "aabBccDDEE", 
    "aaBBccdDEE", "aabBccdDEE", "aaBBccDDeE", "aabBccDDeE", "aaBBccdDeE", "aabBccdDeE", 
    "AAbbccDDEE", "aAbbccDDEE", "AAbbccdDEE", "aAbbccdDEE", "AAbbccDDeE", "aAbbccDDeE", 
    "AAbbccdDeE", "aAbbccdDeE", "aabbccDDEE", "aabbccdDEE", "aabbccDDeE", "aabbccdDeE", 
    "AABBCCddEE", "aABBCCddEE", "AAbBCCddEE", "aAbBCCddEE", "AABBcCddEE", "aABBcCddEE", 
    "AAbBcCddEE", "aAbBcCddEE", "AABBCCddeE", "aABBCCddeE", "AAbBCCddeE", "aAbBCCddeE", 
    "AABBcCddeE", "aABBcCddeE", "AAbBcCddeE", "aAbBcCddeE", "aaBBCCddEE", "aabBCCddEE", 
    "aaBBcCddEE", "aabBcCddEE", "aaBBCCddeE", "aabBCCddeE", "aaBBcCddeE", "aabBcCddeE", 
    "AAbbCCddEE", "aAbbCCddEE", "AAbbcCddEE", "aAbbcCddEE", "AAbbCCddeE", "aAbbCCddeE", 
    "AAbbcCddeE", "aAbbcCddeE", "aabbCCddEE", "aabbcCddEE", "aabbCCddeE", "aabbcCddeE", 
    "AABBccddEE", "aABBccddEE", "AAbBccddEE", "aAbBccddEE", "AABBccddeE", "aABBccddeE", 
    "AAbBccddeE", "aAbBccddeE", "aaBBccddEE", "aabBccddEE", "aaBBccddeE", "aabBccddeE", 
    "AAbbccddEE", "aAbbccddEE", "AAbbccddeE", "aAbbccddeE", "aabbccddEE", "aabbccddeE", 
    "AABBCCDDee", "aABBCCDDee", "AAbBCCDDee", "aAbBCCDDee", "AABBcCDDee", "aABBcCDDee", 
    "AAbBcCDDee", "aAbBcCDDee", "AABBCCdDee", "aABBCCdDee", "AAbBCCdDee", "aAbBCCdDee", 
    "AABBcCdDee", "aABBcCdDee", "AAbBcCdDee", "aAbBcCdDee", "aaBBCCDDee", "aabBCCDDee", 
    "aaBBcCDDee", "aabBcCDDee", "aaBBCCdDee", "aabBCCdDee", "aaBBcCdDee", "aabBcCdDee", 
    "AAbbCCDDee", "aAbbCCDDee", "AAbbcCDDee", "aAbbcCDDee", "AAbbCCdDee", "aAbbCCdDee", 
    "AAbbcCdDee", "aAbbcCdDee", "aabbCCDDee", "aabbcCDDee", "aabbCCdDee", "aabbcCdDee", 
    "AABBccDDee", "aABBccDDee", "AAbBccDDee", "aAbBccDDee", "AABBccdDee", "aABBccdDee", 
    "AAbBccdDee", "aAbBccdDee", "aaBBccDDee", "aabBccDDee", "aaBBccdDee", "aabBccdDee", 
    "AAbbccDDee", "aAbbccDDee", "AAbbccdDee", "aAbbccdDee", "aabbccDDee", "aabbccdDee", 
    "AABBCCddee", "aABBCCddee", "AAbBCCddee", "aAbBCCddee", "AABBcCddee", "aABBcCddee", 
    "AAbBcCddee", "aAbBcCddee", "aaBBCCddee", "aabBCCddee", "aaBBcCddee", "aabBcCddee", 
    "AAbbCCddee", "aAbbCCddee", "AAbbcCddee", "aAbbcCddee", "aabbCCddee", "aabbcCddee", 
    "AABBccddee", "aABBccddee", "AAbBccddee", "aAbBccddee", "aaBBccddee", "aabBccddee", 
    "AAbbccddee", "aAbbccddee", "aabbccddee"
)

(locA, locB, locC, locD, locE) = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('A', (('A', locA), )), ('a', (('a', locA), )),
    ('B', (('B', locB), )), ('b', (('b', locB), )),
    ('C', (('C', locC), )), ('c', (('c', locC), )),
    ('D', (('D', locD), )), ('d', (('d', locD), )),
    ('E', (('E', locE), )), ('e', (('e', locE), ))
))
FMS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts (gRNA)
###############################################################################
HLT_DICT = OrderedDict((
    ('T*',   (('A', locA), ('B', locB), ('C', locC), ('D', locD), ('E', locE))),
    ('O-',   (('a', locA), ('b', locB), ('c', locC), ('d', locD), ('e', locE)))
))
FMS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

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
    ('O*', (('A', locA), ('B', locB), ('C', locC), ('D', locD))),
    ('W-', (('a', locA), ('b', locB), ('c', locC), ('d', locD)))
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
    return (aggD, yRange, 'ifegenia_5')
