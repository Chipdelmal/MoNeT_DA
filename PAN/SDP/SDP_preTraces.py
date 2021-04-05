

import sys
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import SDP_aux as aux
import SDP_gene as drv
import SDP_land as lnd
from joblib import Parallel, delayed


if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'IIT', 'ECO')
    JOB = aux.JOB_DSK
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
    JOB = aux.JOB_SRV
###############################################################################
# Setting up paths and style
###############################################################################
EXPS = aux.EXPS
for exp in EXPS:
    (drive, land) = (
        drv.driveSelector(DRV, AOI, popSize=aux.POP_SIZE), lnd.landSelector()
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
        PT_PRE, PT_IMG, tS, aux.XP_ID+' Pretraces {} [{}]'.format(DRV, AOI)
    )
    ###########################################################################
    # Style 
    ###########################################################################
    (CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
    STYLE = {
            "width": .75, "alpha": .75, "dpi": 300, "legend": True,
            "aspect": .25, "colors": CLR, "xRange": aux.XRAN, 'yRange': YRAN
        }
    STYLE['aspect'] = monet.scaleAspect(1, STYLE)
    ###########################################################################
    # Load preprocessed files lists
    ###########################################################################
    tyTag = ('sum', 'srp')
    (fltrPattern, globPattern) = ('dummy', PT_PRE+'*'+AOI+'*'+'{}'+'*')
    if aux.FZ:
        fltrPattern = aux.patternForReleases('00', AOI, '*')
    fLists = monet.getFilteredTupledFiles(
        PT_PRE+fltrPattern, globPattern, tyTag
    )
    ###########################################################################
    # Process files
    ###########################################################################
    Parallel(n_jobs=JOB)(
        delayed(monet.exportPreTracesPlotWrapper)(
            exIx, fLists, STYLE, PT_IMG
        ) for exIx in range(0, len(fLists))
    )
    # Export gene legend ------------------------------------------------------
    sumDta = pkl.load(fLists[-1][0])
    cl = [i[:-2]+'cc' for i in CLR]
    monet.exportGeneLegend(
        sumDta['genotypes'], cl, 
        PT_IMG+'/legend_{}.png'.format(AOI), 500
    )
