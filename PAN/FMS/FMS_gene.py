#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import FMS_gene_FMS as FMS
import FMS_gene_PGS as PGS
import FMS_gene_IIT as IIT
import FMS_gene_RDL as RDL
import FMS_gene_RDF as RDF
import FMS_aux as aux

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    if (DRIVE == 'FMS'):
        (aggD, yRange, folder) = FMS.driveParameters(TYPE, popSize)
    elif (DRIVE == 'PGS'):
        (aggD, yRange, folder) = PGS.driveParameters(TYPE, popSize)
    elif (DRIVE == 'IIT'):
        (aggD, yRange, folder) = IIT.driveParameters(TYPE, popSize)
    elif (DRIVE == 'RDL'):
        (aggD, yRange, folder) = RDL.driveParameters(TYPE, popSize)
    elif (DRIVE == 'RDF'):
        (aggD, yRange, folder) = RDF.driveParameters(TYPE, popSize)
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
