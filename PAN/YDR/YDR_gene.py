
import YDR_gene_ASD as ASD
import YDR_gene_XSD as XSD
import YDR_gene_YSD as YSD
import YDR_gene_AXS as AXS
import YDR_gene_YXS as YXS
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
#   Ecology, Health, Trash, Wild
###############################################################################
COLEN = ['#2614ed', '#FF006E', '#45d40c', '#8338EC', '#1888e3', '#BC1097', '#FFE93E', '#3b479d']
COLHN = ['#FF006E', '#8338EC', '#0C4887']
COLTN = ['#00a2fe', '#8338EC', '#0C4887']
COLWN = ['#0eeb10', '#8338EC', '#0C4887']
# Auto-generate colorsets with required alphas --------------------------------
(COLEN, COLHN, COLTN, COLWN) = [monet.addHexOpacity(i, alpha='1A') for i in (COLEN, COLHN, COLTN, COLWN)]
(COLEO, COLHO, COLTO, COLWO) = [monet.replaceHexOpacity(i, alpha='FF') for i in (COLEN, COLHN, COLTN, COLWN)]
(COLEM, COLHM, COLTM, COLWM) = [monet.generateAlphaColorMapFromColorArray(COLWO) for i in (COLEO, COLHO, COLTO, COLWO)]


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=11000):
    ###########################################################################
    # Autosomal Split Drive ---------------------------------------------------
    if DRIVE == 'ASD':
        (aggD, yRange, folder) = ASD.driveParameters(TYPE, popSize)
    # X-Linked Split Drive ----------------------------------------------------
    if DRIVE == 'XSD':
        (aggD, yRange, folder) = XSD.driveParameters(TYPE, popSize)
    # Y-Linked Split Drive ----------------------------------------------------
    if DRIVE == 'YSD':
        (aggD, yRange, folder) = YSD.driveParameters(TYPE, popSize)
    # Autosomal X-Shredder ----------------------------------------------------
    if DRIVE == 'AXS':
        (aggD, yRange, folder) = AXS.driveParameters(TYPE, popSize)
    # Autosomal Y-Shredder ----------------------------------------------------
    if DRIVE == 'YXS':
        (aggD, yRange, folder) = YXS.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = COLEN
    elif TYPE == 'HLT':
        colors = COLHN
    elif TYPE == 'TRS':
        colors = COLTN
    elif TYPE == 'WLD':
        colors = COLWN
    ###########################################################################
    if TYPE != 'ECO':
        yRange = yRange / 2
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict
