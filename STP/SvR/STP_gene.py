
import MoNeT_MGDrivE as monet
import STP_gene_LDR as LDR
import STP_gene_Human as HUM

###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(100*12000)):
    ###########################################################################
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'LDR':
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    # Human -------------------------------------------------------------------
    if DRIVE == 'HUM':
        (aggD, yRange, folder) = HUM.driveParameters(TYPE)
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
