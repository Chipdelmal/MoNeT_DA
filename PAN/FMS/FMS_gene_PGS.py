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
    "AABBCCDD", "aABBCCDD", "AAbBCCDD", "aAbBCCDD", "AABBcCDD", "aABBcCDD", 
    "AAbBcCDD", "aAbBcCDD", "AABBCCdD", "aABBCCdD", "AAbBCCdD", "aAbBCCdD", 
    "AABBcCdD", "aABBcCdD", "AAbBcCdD", "aAbBcCdD", "aaBBCCDD", "aabBCCDD", 
    "aaBBcCDD", "aabBcCDD", "aaBBCCdD", "aabBCCdD", "aaBBcCdD", "aabBcCdD", 
    "AAbbCCDD", "aAbbCCDD", "AAbbcCDD", "aAbbcCDD", "AAbbCCdD", "aAbbCCdD", 
    "AAbbcCdD", "aAbbcCdD", "aabbCCDD", "aabbcCDD", "aabbCCdD", "aabbcCdD",
    "AABBccDD", "aABBccDD", "AAbBccDD", "aAbBccDD", "AABBccdD", "aABBccdD", 
    "AAbBccdD", "aAbBccdD", "aaBBccDD", "aabBccDD", "aaBBccdD", "aabBccdD", 
    "AAbbccDD", "aAbbccDD", "AAbbccdD", "aAbbccdD", "aabbccDD", "aabbccdD", 
    "AABBCCdd", "aABBCCdd", "AAbBCCdd", "aAbBCCdd", "AABBcCdd", "aABBcCdd", 
    "AAbBcCdd", "aAbBcCdd", "aaBBCCdd", "aabBCCdd", "aaBBcCdd", "aabBcCdd", 
    "AAbbCCdd", "aAbbCCdd", "AAbbcCdd", "aAbbcCdd", "aabbCCdd", "aabbcCdd", 
    "AABBccdd", "aABBccdd", "AAbBccdd", "aAbBccdd", "aaBBccdd", "aabBccdd", 
    "AAbbccdd", "aAbbccdd", "aabbccdd"
)
(locA, locB, locC, locD) = ((0, 1), (2, 3), (4, 5), (6, 7))

###############################################################################
# Ecology genotype counts
###############################################################################
ECO_DICT = OrderedDict((
    ('A', (('A', locA), )), ('a', (('a', locA), )),
    ('B', (('B', locB), )), ('b', (('b', locB), )),
    ('C', (('C', locC), )), ('c', (('c', locC), )),
    ('D', (('D', locD), )), ('d', (('d', locD), ))
))
PGS_ECO = monet.geneFrequencies(ECO_DICT, genotypes)

###############################################################################
# Health genotype counts (gRNA)
###############################################################################
HLT_DICT = OrderedDict((
    ('gRNA*',   (('B', locB), )),
    ('O-',      (('b', locB), ))
))
PGS_HLT = monet.carrierFrequencies(HLT_DICT, genotypes)

###############################################################################
# Trash genotype counts (Cas9)
###############################################################################
TRS_DICT = OrderedDict((
    ('Cas9*',   (('A', locA), )),
    ('O-',      (('a', locA), ))
))
PGS_TRS = monet.carrierFrequencies(TRS_DICT, genotypes)

###############################################################################
# Wild genotype counts
###############################################################################
WLD_DICT = OrderedDict((
    ('O*', (('A', locA), ('B', locB), ('C', locC), ('D', locD))),
    ('W-', (('a', locA), ('b', locB), ('c', locC), ('d', locD)))
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
        yRange = popSize/2
    elif TYPE == 'TRS':
        aggD = monet.generateAggregationDictionary(*PGS_TRS)
        yRange = popSize/2
    elif TYPE == 'WLD':
        aggD = monet.generateAggregationDictionary(*PGS_WLD)
        yRange = popSize/2
    return (aggD, yRange, 'pgSIT')
