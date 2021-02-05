


import MoNeT_MGDrivE as monet
import PYF_gene_pgSIT as pgs

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'PGS':
        (aggD, yRange, folder) = pgs.driveParameters(TYPE, popSize)
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
        'gDict': aggD, 'yRange': yRange,  'colors': colors, 'folder': folder
    }
    return geneDict


def colorSelector(AOI):
    if AOI == 'ECO':
        colors = monet.COLEO
    elif AOI == 'HLT':
        colors = monet.COLHO
    elif AOI == 'TRS':
        colors = monet.COLTO
    elif AOI == 'WLD':
        colors = monet.COLWO
    elif AOI == 'HUM':
        colors = monet.COLHO
    return colors