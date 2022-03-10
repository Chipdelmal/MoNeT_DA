#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet

genotypes = ('inc_1', 'TOTAL')
allGeneIx = list(range(len(genotypes[0])))
###############################################################################
# Health genotype counts
###############################################################################
HUM_INC = (['I', 'Total', 'Total'], [[0, ], [1, ], [1, ]])

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize=750):
    if TYPE == 'INC':
        aggD = monet.generateAggregationDictionary(
            ['I', 'Total', 'Total'], HUM_INC
        )
    yRange = popSize
    return (aggD, yRange, 'INC')