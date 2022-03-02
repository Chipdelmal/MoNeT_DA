#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet

genotypes = ('inc_1', 'TOTAL')
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Health genotype counts
###############################################################################
sGenes = (('TOTAL', allGeneIx), )
sPos = set(monet.aggregateGeneAppearances(genotypes, sGenes))
iGenes = (('inc_i', allGeneIx), )
iPos = set(monet.aggregateGeneAppearances(genotypes, iGenes))
HUM_INC= [list(i) for i in (iPos, sPos-iPos, sPos|iPos)]

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize=750):
    if TYPE == 'INC':
        aggD = monet.generateAggregationDictionary(
            ['I', 'O', 'Total'], HUM_INC
        )
    yRange = popSize
    return (aggD, yRange, 'INC')