
import MoNeT_MGDrivE as monet
import QLD_gene_IIT as IIT


###############################################################################
# Drive
###############################################################################
def driveSelector(DRV, AOI, popSize=10000):
    # Drive Selection ---------------------------------------------------------
    if DRV == 'IIT':
        (aggD, yRange, folder) = IIT.driveParameters(AOI, popSize)
    # Colors ------------------------------------------------------------------
    if AOI == 'ECO':
        colors = monet.COLEN
    elif AOI == 'HLT':
        colors = monet.COLHN
    elif AOI == 'TRS':
        colors = monet.COLTN
    elif AOI == 'WLD':
        colors = monet.COLWN
    # Return ------------------------------------------------------------------
    gD = {'gDict': aggD, 'yRange': yRange, 'colors': colors, 'folder': folder}
    return gD