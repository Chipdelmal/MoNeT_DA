
import MoNeT_MGDrivE as monet
import v2_gene_SDR as SDR
import v2_gene_HUM as HUM


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=11000):
    ###########################################################################
    # Autosomal Split Drive ---------------------------------------------------
    if DRIVE == 'SDR':
        (aggD, yRange, folder) = SDR.driveParameters(TYPE, popSize)
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
        colors = ['#0eeb101A', '#2614ed1A', '#0C48871A']
    ###########################################################################
    if TYPE != 'ECO':
        yRange = yRange/2
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict
