#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import FMS_gene_FMS3 as FMS3
import FMS_gene_FMS4 as FMS4
import FMS_gene_FMS5 as FMS5
import FMS_gene_PGS as PGS
import FMS_gene_IIT as IIT
import FMS_gene_RDL as RDL
import FMS_gene_RDF as RDF

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    if (DRIVE == 'FMS3'):
        (aggD, yRange, folder) = FMS3.driveParameters(TYPE, popSize)
    elif (DRIVE == 'FMS4'):
        (aggD, yRange, folder) = FMS4.driveParameters(TYPE, popSize)
    elif (DRIVE == 'FMS5'):
        (aggD, yRange, folder) = FMS5.driveParameters(TYPE, popSize)
    elif (DRIVE == 'PGS'):
        (aggD, yRange, folder) = PGS.driveParameters(TYPE, popSize)
    elif (DRIVE == 'IIT'):
        (aggD, yRange, folder) = IIT.driveParameters(TYPE, popSize)
    elif (DRIVE == 'RDL'):
        (aggD, yRange, folder) = RDL.driveParameters(TYPE, popSize)
    elif (DRIVE == 'RDF'):
        (aggD, yRange, folder) = RDF.driveParameters(TYPE, popSize)
    else:
        print("Error in gene drive ID")
    ###########################################################################
    if TYPE == 'ECO':
        colors = [
            '#2614ed55', '#FF006E55', '#45d40c55', '#8338EC55', '#1888e355', 
            '#BC109755', '#FFE93E55', '#3b479d55', '#540d6e55', '#7bdff255'
        ]
    elif TYPE == 'HLT':
        if DRIVE == 'FMS3':
            colors = ['#1888e300', '#2614ed00', '#f2008935']
        elif DRIVE == 'FMS4':
            colors = ['#1888e300', '#2614ed00', '#3b479d35']
        elif DRIVE == 'FMS5':
            colors = ['#1888e300', '#2614ed00', '#45d40c35']
        elif DRIVE == 'PGS':
            colors = ['#1888e300', '#2614ed00', '#8338EC35']
        elif DRIVE == 'IIT':
            colors = ['#f2008900', '#c879ff00', '#540d6e35']
        elif DRIVE == 'RDL':
            colors = ['#f2008900', '#c879ff00', '#bbdefb35']
        elif DRIVE == 'RDF':
            colors = ['#f2008900', '#c879ff00', '#03045e35']
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
