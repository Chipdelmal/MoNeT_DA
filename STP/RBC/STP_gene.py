#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import STP_gene_LDR as LDR
import STP_gene_LDR as SDR

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'LDR':
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    elif DRIVE == 'SDR':
        (aggD, yRange, folder) = SDR.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = monet.COLEN
    elif TYPE == 'HLT':
        colors = monet.COLHN
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'HUM':
        colors = monet.COLHN
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict


def maleFemaleSelector(AOI):
    if AOI == 'HLT':
        MF = (False, True)
    else:
        MF =    (True, True)
    return MF


def colorSelector(AOI):
    if AOI == 'ECO':
        colors = monet.COLEO
    elif AOI == 'HLT':
        colors = monet.COLHO
    elif AOI == 'TRS':
        colors = monet.COLTO
    elif AOI == 'WLD':
        colors = monet.COLWO
    return colors