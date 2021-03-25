

import sys
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'IIT', 'ECO')
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
###############################################################################
EXPS = ('000', '001', '010')
(FZ, FLTR) = (True, ['*', '*', '*', '00', '*', AOI, '*', '{}', 'bz'])
###############################################################################
# Setting up paths and style
###############################################################################
exp = EXPS[0]
for exp in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=25e3), lnd.landSelector()
    )
    (gene, fldr) = (drive.get('gDict'), drive.get('folder'))
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(
        USR, fldr, exp
    )
    PT_IMG = PT_IMG + 'preTraces/'
    monet.makeFolder(PT_IMG)
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    monet.printExperimentHead(
        PT_PRE, PT_IMG, tS, 'SDP Pretraces {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .75, "alpha": .75, "dpi": 300, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": [0, (365*2.5)],
            "yRange": YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if FZ:
        fltrPattern = aux.XP_PTRN.format(*FLTR)
    fLists = monet.getFilteredTupledFiles(
        PT_PRE+fltrPattern, globPattern, tyTag
    )
    ###########################################################################
    # Process files
    ###########################################################################
    (xpNum, digs) = monet.lenAndDigits(fLists)
    i = 0
    for i in range(0, xpNum):
        monet.printProgress(i+1, xpNum, digs)
        (sumDta, repDta) = [pkl.load(file) for file in (fLists[i])]
        name = fLists[i][0].split('/')[-1].split('.')[0][:-4]
        # Export plots --------------------------------------------------------
        monet.exportTracesPlot(repDta, name, STYLE, PT_IMG, wopPrint=False)
        cl = [i[:-2]+'cc' for i in CLR]
    # Export gene legend ------------------------------------------------------
    monet.exportGeneLegend(
        sumDta['genotypes'], cl, PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
