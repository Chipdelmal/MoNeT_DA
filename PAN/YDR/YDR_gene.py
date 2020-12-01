
import YDR_gene_ASD as ASD
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Ecology ---------------------------------------------------------------------
COLEN = ['#2614ed', '#FF006E', '#45d40c', '#8338EC', '#1888e3', '#BC1097']
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
        (aggD, yRange) = ASD.driveParameters(TYPE, popSize)
    # X-Linked Split Drive ----------------------------------------------------
    # Y-Linked Split Drive ----------------------------------------------------
    # Autosomal X-Shredder ----------------------------------------------------
    # Autosomal Y-Shredder ----------------------------------------------------
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
    return {'gDict': aggD, 'yRange': yRange, 'colors': colors}
