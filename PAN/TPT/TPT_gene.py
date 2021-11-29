#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import TPT_gene_LDR as LDR
import TPT_gene_HUM as HUM

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000), humSize=352e3):
    ###########################################################################
    if TYPE != 'HUM':
        if DRIVE == 'LDR':
            (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    else:
        # Human ---------------------------------------------------------------
        (aggD, yRange, folder) = HUM.driveParameters(TYPE, popSize=humSize)
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
    if (AOI == 'HLT') or (AOI == 'HUM'):
        MF = (False, True)
    else:
        MF =    (True, True)
    return MF

1

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