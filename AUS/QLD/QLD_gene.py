
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
        colors = ['#FF006E0B', '#8338EC0A', '#0C48871F'] # monet.COLHN
    elif AOI == 'TRS':
        colors = monet.COLTN
    elif AOI == 'WLD':
        colors = monet.COLWN
    # Return ------------------------------------------------------------------
    gD = {'gDict': aggD, 'yRange': yRange, 'colors': colors, 'folder': folder}
    return gD


def maleFemaleSelector(AOI):
    if AOI == 'HLT':
        MF = (False, True)
    else:
        MF =    (True, True)
    return MF