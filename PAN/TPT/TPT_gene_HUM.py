#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import MoNeT_MGDrivE as monet

genotypes = ('S', 'I')

###############################################################################
# Health genotype counts
###############################################################################
HUM_HLT = (['S', 'Prev.', 'Total'], [[0, ], [1, ], [1, ]])

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize=360000):
    if TYPE == 'HUM':
        aggD = monet.generateAggregationDictionary(*HUM_HLT)
    yRange = popSize
    return (aggD, yRange, 'HUM')
