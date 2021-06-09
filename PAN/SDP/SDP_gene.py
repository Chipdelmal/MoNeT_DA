
import MoNeT_MGDrivE as monet
import SDP_gene_AXS as AXS
import SDP_gene_CRS as CRS
import SDP_gene_CRS as CRX
import SDP_gene_CRS as CRY
import SDP_gene_FSR as FSR
import SDP_gene_IIT as IIT
import SDP_gene_PGS as PGS
import SDP_gene_SDR as SDR
import SDP_gene_SDR as SDX
import SDP_gene_SDR as SDY
import SDP_gene_SIT as SIT

###############################################################################
# Drive
###############################################################################
def driveSelector(DRV, AOI, popSize=10000):
    # Drive Selection ---------------------------------------------------------
    if DRV == 'IIT':
        (aggD, yRange, folder) = IIT.driveParameters(AOI, popSize)
    if DRV == 'FSR':
        (aggD, yRange, folder) = FSR.driveParameters(AOI, popSize)
    if DRV == 'PGS':
        (aggD, yRange, folder) = PGS.driveParameters(AOI, popSize)
    if DRV == 'AXS':
        (aggD, yRange, folder) = AXS.driveParameters(AOI, popSize)
    if DRV == 'CRX':
        (aggD, yRange, folder) = CRX.driveParameters(AOI, popSize)
    if DRV == 'CRY':
        (aggD, yRange, folder) = CRY.driveParameters(AOI, popSize)
    if DRV == 'SDX':
        (aggD, yRange, folder) = SDX.driveParameters(AOI, popSize)
    if DRV == 'SDY':
        (aggD, yRange, folder) = SDY.driveParameters(AOI, popSize)
    if DRV == 'CRS':
        (aggD, yRange, folder) = CRS.driveParameters(AOI, popSize)
    if DRV == 'SDR':
        (aggD, yRange, folder) = SDR.driveParameters(AOI, popSize)
    if DRV == 'SIT':
        (aggD, yRange, folder) = SIT.driveParameters(AOI, popSize)
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
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict