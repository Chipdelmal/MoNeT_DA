#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import GOP_gene_PGS as PGS
import GOP_gene_EPI as EPI

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000), humSize=10000):
    ###########################################################################
    if (DRIVE == 'HUM'):
        (aggD, yRange, folder) = EPI.driveParameters(TYPE, popSize)
    elif (DRIVE == 'PGS'):
        (aggD, yRange, folder) = PGS.driveParameters(TYPE, popSize)
    else:
        print("Error in gene drive ID")
    ###########################################################################
    if TYPE == 'ECO':
        colors = [
            '#2614ed55', '#FF006E55', '#45d40c55', '#8338EC55', '#1888e355', 
            '#BC109755', '#FFE93E55', '#3b479d55', '#540d6e55', '#7bdff255'
        ]
    elif TYPE == 'HLT':
        colors = ['#f2008955', '#c879ff55', '#2614ed35']
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'HUM':
        colors = ['#274c7735', '#c879ff99', '#dee2ff35']
    elif TYPE == 'CSS':
        colors = ['#8CD9FF53', '#bbdefb55', '#dee2ff35']
    elif TYPE == 'MRT':
        colors = ['#274c7735', '#c879ff99', '#dee2ff35']
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 'colors': colors, 'folder': folder
    }
    return geneDict

def maleFemaleSelector(AOI):
    if (AOI == 'HLT') or (AOI == 'INC'):
        MF = (False, True)
    elif (AOI == 'HUM'):
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
