
import YDR_gene_ASD as ASD
import YDR_gene_XSD as XSD
import YDR_gene_YSD as YSD
import YDR_gene_AXS as AXS
import YDR_gene_YXS as YXS
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Ecology ---------------------------------------------------------------------
COLEN = [
    '#2614ed', '#FF006E', '#45d40c', '#8338EC', 
    '#1888e3', '#BC1097', '#FFE93E', '#3b479d'
]
COLEN = [c+'1A' for c in COLEN]
COLEO = [i[:-2]+'FF' for i in COLEN]
COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
# Health ----------------------------------------------------------------------
COLHN = ['#FF006E', '#8338EC', '#0C4887']
COLHN = [c+'1A' for c in COLHN]
COLHO = [i[:-2]+'FF' for i in COLHN]
COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Trash ----------------------------------------------------------------------
COLTN = ['#00a2fe', '#8337ec', '#0C4887']
COLTN = [c+'1A' for c in COLTN]
COLTO = [i[:-2]+'FF' for i in COLTN]
COLTM = monet.generateAlphaColorMapFromColorArray(COLTO)
# Wild ----------------------------------------------------------------------
COLWN = ['#0eeb10', '#8337ec', '#0C4887']
COLWN = [c+'1A' for c in COLWN]
COLWO = [i[:-2]+'FF' for i in COLWN]
COLWM = monet.generateAlphaColorMapFromColorArray(COLWO)


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
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict
