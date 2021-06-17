
import MoNeT_MGDrivE as monet
import SDP_gene_AXS as AXS
import SDP_gene_CRS as CRS
import SDP_gene_CRX as CRX
import SDP_gene_CRY as CRY
import SDP_gene_FSR as FSR
import SDP_gene_IIT as IIT
import SDP_gene_PGS as PGS
import SDP_gene_SDR as SDR
import SDP_gene_SDX as SDX
import SDP_gene_SDY as SDY
import SDP_gene_SIT as SIT

###############################################################################
# Drive
###############################################################################
def driveSelector(DRV, AOI, popSize=10000):
    # Colors ------------------------------------------------------------------
    if AOI == 'TPS':
        if DRV == 'IIT':
            colors = ['#FF006E00', '#8338EC00', '#0C4887']
        elif DRV == 'FSR':
            colors = ['#FF006E00', '#8338EC00', '#2614ed']
        elif DRV == 'PGS':
            colors = ['#FF006E00', '#8338EC00', '#FF006E']
        elif DRV == 'AXS':
            colors = ['#FF006E00', '#8338EC00', '#45d40c']
        elif DRV == 'CRX':
            colors = ['#FF006E00', '#8338EC00', '#8338EC']
        elif DRV == 'CRY':
            colors = ['#FF006E00', '#8338EC00', '#1888e3']
        elif DRV == 'SDX':
            colors = ['#FF006E00', '#8338EC00', '#BC1097']
        elif DRV == 'SDY':
            colors = ['#FF006E00', '#8338EC00', '#FFE93E']
        elif DRV == 'CRS':
            colors = ['#FF006E00', '#8338EC00', '#FFAE42']
        elif DRV == 'SDR':
            colors = ['#FF006E00', '#8338EC00', '#00FA9A']
        elif DRV == 'SIT':
            colors = ['#FF006E00', '#8338EC00', '#ED1C24']
        else:
            colors = ['#FF006E00', '#8338EC00', '#808080']
    else:
        if AOI == 'ECO':
            colors = monet.COLEN
        elif AOI == 'HLT':
            colors = monet.COLHN
        elif AOI == 'TRS':
            colors = monet.COLTN
        elif AOI == 'WLD':
            colors = monet.COLWN
    # Drive Selection ---------------------------------------------------------
    if AOI == 'TPS':
        AOI = 'HLT'
    # 
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
    # Return ------------------------------------------------------------------
    geneDict = {
        'gDict': aggD, 'yRange': yRange,
        'colors': colors, 'folder': folder
    }
    return geneDict
