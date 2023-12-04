#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import TPP_gene_LDR as LDR
import TPP_gene_EPI as EPI

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(int(50e6*2.5)), humSize=10000):
    ###########################################################################
    if (DRIVE == 'HUM'):
        (aggD, yRange, folder) = EPI.driveParameters(TYPE, popSize)
    elif (DRIVE == 'LDR'):
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    else:
        print("Error in gene drive ID")
    ###########################################################################
    if TYPE == 'ECO':
        colors = [
            '#4E425355', '#D96B7255', '#89C07455', '#4F70A955', 
            '#F7E2B955' 
        ]
    elif TYPE == 'HLT':
        colors = ['#B75B5944', '#43486944', '#EAD6BA00']
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'HUM':
        colors = ['#274c7735', '#c879ff99', '#dee2ff35']
    elif TYPE[:3] == 'CSS':
        colors = ['#FF006E55', '#540d6e22', '#1d355799']
    elif TYPE[:3] == 'MRT':
        colors = ['#45d40c55', '#c879ff22', '#1d355799']
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
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
