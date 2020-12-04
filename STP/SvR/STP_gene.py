
import MoNeT_MGDrivE as monet
import STP_gene_LDR as LDR

###############################################################################
# Colors
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
def driveSelector(DRIVE, TYPE, popSize=110000):
    # Linked Drive ------------------------------------------------------------
    if DRIVE == 'LDR':
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
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
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict