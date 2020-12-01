
import MoNeT_MGDrivE as monet

genotypes = (
    'XXWW','XXWG','XXWR','XXWB','XXGG','XXGR','XXGB','XXRR','XXRB','XXBB',
    'XCWW','XCWG','XCWR','XCWB','XCGG','XCGR','XCGB','XCRR','XCRB','XCBB',
    'CCWW','CCWG','CCWR','CCWB','CCGG','CCGR','CCGB','CCRR','CCRB','CCBB',
    'XYWW','XYWG','XYWR','XYWB','XYGG','XYGR','XYGB','XYRR','XYRB','XYBB',
    'CYWW','CYWG','CYWR','CYWB','CYGG','CYGR','CYGB','CYRR','CYRB','CYBB'
)
allGeneIx = list(range(len(genotypes[0])))

###############################################################################
# Ecology genotype counts
###############################################################################
xGenes = (('X', allGeneIx), )
xPos = monet.aggregateGeneAppearances(genotypes, xGenes)
yGenes = (('Y', allGeneIx), )
yPos = monet.aggregateGeneAppearances(genotypes, yGenes)
cGenes = (('C', allGeneIx), )
cPos = monet.aggregateGeneAppearances(genotypes, cGenes)
wGenes = (('W', allGeneIx), )
wPos = monet.aggregateGeneAppearances(genotypes, wGenes)
gGenes = (('G', allGeneIx), )
gPos = monet.aggregateGeneAppearances(genotypes, gGenes)
rGenes = (('R', allGeneIx), )
rPos = monet.aggregateGeneAppearances(genotypes, rGenes)
bGenes = (('B', allGeneIx), )
bPos = monet.aggregateGeneAppearances(genotypes, bGenes)
XSD_ECO = (xPos, yPos, cPos, wPos, gPos, rPos, bPos)