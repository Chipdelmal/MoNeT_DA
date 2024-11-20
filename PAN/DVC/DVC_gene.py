#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import DVC_gene_PGS as PGS

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    if (DRIVE == 'DVC'):
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
        if DRIVE == 'PGS':
            colors = ['#1888e355', '#2614ed55', '#f2008935']
        else:
            colors = ['#f2008955', '#c879ff55', '#c879ff35']
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'HUM':
        colors = ['#274c7700', '#c879ff99', '#dee2ff55']
    elif TYPE == 'INC':
        colors = ['#8CD9FF00', '#bbdefb55', '#dee2ff00']
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
