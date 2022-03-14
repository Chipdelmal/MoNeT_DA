#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import TPT_gene_LDR as LDR
import TPT_gene_HUM as HUM
import TPT_gene_INC as INC

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000), humSize=352e3):
    ###########################################################################
    if (TYPE == 'HUM'):
        (aggD, yRange, folder) = HUM.driveParameters(TYPE, popSize=humSize)
    elif (TYPE == 'INC'):
        (aggD, yRange, folder) = INC.driveParameters(TYPE, popSize=1000)
    else:
        if (DRIVE == 'LDR'):
            (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = monet.COLEN
    elif TYPE == 'HLT':
        colors = ['#f2008955', '#0d47a155', '#d6d6d611']
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'HUM':
        colors = ['#274c7700', '#c879ff55', '#dee2ff55']
    elif TYPE == 'INC':
        colors = ['#8CD9FF15', '#5D81EA00', '#dee2ff00']
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 'colors': colors, 'folder': folder
    }
    return geneDict


def maleFemaleSelector(AOI):
    if (AOI == 'HLT') or (AOI == 'HUM') or (AOI == 'INC'):
        MF = (False, True)
    else:
        MF = (True, True)
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