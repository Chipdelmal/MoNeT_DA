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
        colors = ['#B75B5944', '#43486944', '#B36FA000']
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'CSS':
        colors = ['#D1C87A22', '#CA5E5022', '#43486988']
    elif TYPE == 'MRT':
        colors = ['#6E855C22', '#56799322', '#43486988']
    elif TYPE == 'PRV':
        colors = ['#F1B15222', '#80A08E22', '#43486988']
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
