
import tGD_gene_tGD as TGD
import tGD_gene_split as SDR
import tGD_gene_linked as LDR
import tGD_gene_clvr as clv
import MoNeT_MGDrivE as monet


###############################################################################
# Colors
###############################################################################
# Ecology ---------------------------------------------------------------------
COLEN = [
        "#2614ed", "#FF006E", "#45d40c",
        "#8338EC", "#1888e3", "#BC1097"
    ]
COLEN = [c+'1A' for c in COLEN]
COLEO = [i[:-2]+'FF' for i in COLEN]
# COLEM = monet.generateAlphaColorMapFromColorArray(COLEO)
# Health ----------------------------------------------------------------------
COLHN = ["#FF006E1A", "#8338EC00", "#0C48871A"]
# COLHN = [c+'1A' for c in COLHN]
COLHO = [i[:-2]+'FF' for i in COLHN]
# COLHM = monet.generateAlphaColorMapFromColorArray(COLHO)
# Trash ----------------------------------------------------------------------
COLTN = ["#BC1097", "#8337ec", "#0C4887"]
# COLTN = [c+'1A' for c in COLTN]
COLTO = [i[:-2]+'FF' for i in COLTN]
# COLTM = monet.generateAlphaColorMapFromColorArray(COLTO)
# Wild ----------------------------------------------------------------------
COLWN = ["#8337ec", "#00a2fe", "#0C4887"]
COLWN = [c+'1A' for c in COLWN]
COLWO = [i[:-2]+'FF' for i in COLWN]
# COLWM = monet.generateAlphaColorMapFromColorArray(COLWO)
# CLS ----------------------------------------------------------------------
COLCN = ["#0eeb101A", "#00a2fe00", "#0C488700"]
# COLCN = [c+'AA' for c in COLCN]
COLCO = [i[:-2]+'FF' for i in COLCN]
# COLCM = monet.generateAlphaColorMapFromColorArray(COLCO)


###############################################################################
# Drive
###############################################################################
def driveSelector(DRIVE, TYPE, popSize=(11000)):
    if DRIVE == 'linkedDrive':
        (aggD, yRange, folder) = LDR.driveParameters(TYPE, popSize)
    elif DRIVE == 'splitDrive':
        (aggD, yRange, folder) = SDR.driveParameters(TYPE, popSize)
    elif DRIVE == 'tGD':
        (aggD, yRange, folder) = TGD.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = monet.COLEN
    elif TYPE == 'HLT':
        colors = COLHN
    elif TYPE == 'TRS':
        colors = monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    elif TYPE == 'CST':
        colors = COLCN
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict