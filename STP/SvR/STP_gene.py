
import MoNeT_MGDrivE as monet
import STP_gene_LDR as LDR


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'LDR':
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = monet.COLEN
    elif TYPE == 'HLT':
        colors = monet.COLHN
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict