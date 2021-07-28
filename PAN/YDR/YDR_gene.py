
import YDR_gene_ASD as ASD
import YDR_gene_XSD as XSD
import YDR_gene_YSD as YSD
import YDR_gene_AXS as AXS
import YDR_gene_YXS as YXS
import YDR_gene_CRS as CRS
import MoNeT_MGDrivE as monet


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
    # CRISPR ------------------------------------------------------------------
    if DRIVE == 'CRS':
        (aggD, yRange, folder) = CRS.driveParameters(TYPE, popSize)
    ###########################################################################
    if TYPE == 'ECO':
        colors = monet.COLEN
    elif TYPE == 'HLT':
        colors = monet.COLHN
    elif TYPE == 'TRS':
        colors = ['#00a2fe1A', '#8338EC00', '#0C488702'] # monet.COLTN
    elif TYPE == 'WLD':
        colors = monet.COLWN
    ###########################################################################
    if TYPE != 'ECO':
        yRange = yRange/2
    if TYPE == 'TRS':
        yRange = yRange
    ###########################################################################
    geneDict = {
        'gDict': aggD, 'yRange': yRange, 
        'colors': colors, 'folder': folder
    }
    return geneDict
