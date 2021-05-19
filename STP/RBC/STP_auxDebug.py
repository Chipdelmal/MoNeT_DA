
import numpy as np
from os import path
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


###############################################################################
# PreProcess Updates
###############################################################################
def preProcessParallel(
            exIx, expNum,
            drive, analysisOI='HLT', prePath='./',
            nodesAggLst=[[0]], fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=False, SPA=False, REP=False, SRP=True,
            sexFilenameIdentifiers={"male": "M_", "female": "F_"}
        ):
    (ix, expDirsMean, expDirsTrac) = exIx
    monet.printProgress(ix+1, expNum, nodeDigits)
    (pathMean, pathTraces) = (expDirsMean, expDirsTrac+'/')
    expName = pathMean.split('/')[-1]
    fNameFmt = '{}/{}-{}_'.format(prePath, expName, analysisOI)
    monet.preProcessLandscape(
        pathMean, pathTraces, expName, drive, prePath,
        analysisOI=analysisOI, nodesAggLst=nodesAggLst,
        fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers=sexFilenameIdentifiers
    )
    return None


###############################################################################
# PreTraces Updates
###############################################################################
def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    monet.exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth
    )
    return None


###############################################################################
# PstTraces Updates
###############################################################################
def exportPstTracesParallel(
        exIx, expsNum,
        STABLE_T, THS, QNT, STYLE, PT_IMG, 
        border=True, borderColor='#322E2D', borderWidth=1, 
        labelPos=(.7, .9), xpsNum=0, digs=3, 
        autoAspect=False, popScaler=1,
        wopPrint=True, cptPrint=True, poePrint=True,
    ):
    (ix, repFile, tti, tto, wop, mnf, mnd, poe, cpt) = exIx
    repDta = pkl.load(repFile)
    # Print to terminal -------------------------------------------------------
    padi = str(ix+1).zfill(digs)
    fmtStr = '{}+ File: {}/{}'
    print(fmtStr.format(monet.CBBL, padi, expsNum, monet.CEND), end='\r')
    # Traces ------------------------------------------------------------------
    pop = repDta['landscapes'][0][STABLE_T][-1]
    # STYLE['yRange'] = (0,  pop*popScaler)
    monet.exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto, mnd], hLines=[mnf*pop], labelPos=labelPos, 
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        autoAspect=autoAspect, popScaler=1,
        wop=wop, wopPrint=wopPrint, 
        cpt=cpt, cptPrint=cptPrint,
        poe=poe, poePrint=poePrint
    )
    return None


###############################################################################
# PstFraction Updates
###############################################################################
def pstFractionParallel(exIx, PT_OUT, baseFiles, meanFiles, traceFiles):
    (_, bFile, mFile, tFile) = exIx
    # Load data ---------------------------------------------------------------
    (base, trace) = [pkl.load(file) for file in (bFile, tFile)]
    # Process data ------------------------------------------------------------
    fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
    repsRatios = monet.getPopRepsRatios(base, trace, 1)
    np.save(fName, repsRatios)
    return None


###############################################################################
# PstProcess Updates
###############################################################################
def calcMetrics(
        repRto,
        thi=.25, tho=.25, thw=.25, tap=50, thp=(.025, .975),
        finalDay=-1
    ):
    (minS, maxS, _, _) = monet.calcMinMax(repRto)
    mtrRep = {
        'TTI': monet.calcTTI(repRto, thi),
        'TTO': monet.calcTTO(repRto, tho),
        'WOP': monet.calcWOP(repRto, thw),
        'MIN': minS,
        'MAX': maxS,
        'RAP': monet.getRatioAtTime(repRto, tap),
        'POE': monet.calcPOE(repRto, finalDay=finalDay, thresholds=thp),
        'CPT': monet.calcCPT(repRto)
    }
    return mtrRep



def calcMtrQnts(mtrsReps, qnt=0.5):
    ttiSQ = [np.nanquantile(tti, qnt) for tti in mtrsReps['TTI']]
    ttoSQ = [np.nanquantile(tto, 1-qnt) for tto in mtrsReps['TTO']]
    wopSQ = [np.nanquantile(wop, 1-qnt) for wop in mtrsReps['WOP']]
    rapSQ = [np.nanquantile(rap, qnt) for rap in mtrsReps['RAP']]
    mniSQ = (
        np.nanquantile(mtrsReps['MIN'][0], qnt), 
        np.nanquantile(mtrsReps['MIN'][1], qnt)
    )
    mnxSQ = (
        np.nanquantile(mtrsReps['MAX'][0], qnt), 
        np.nanquantile(mtrsReps['MAX'][1], 1-qnt)
    )
    cptSQ = (np.nanquantile(mtrsReps['CPT'], qnt))
    poeSQ = [mtrsReps['POE']]
    # Setup return dictionary -------------------------------------------------
    mtrQnt = {
        'TTI': ttiSQ,
        'TTO': ttoSQ,
        'WOP': wopSQ,
        'RAP': rapSQ,
        'MIN': list(mniSQ)+list(mnxSQ),
        'POE': list(poeSQ[0]),
        'CPT': [cptSQ]
    }
    return mtrQnt


def pstProcessParallel(
        exIx, header, xpidIx,
        thi=.25, tho=.25, thw=.25, tap=50, thp=(.025, .975),
        finalDay=-1, qnt=0.5, POE=True, CPT=True,
        DF_SORT=['TTI', 'TTO', 'WOP', 'RAP', 'MIN', 'POE', 'CPT']
    ):
    (outPaths, fPaths) = exIx
    (fNum, digs) = monet.lenAndDigits(fPaths)
    ###########################################################################
    # Setup dataframes
    ###########################################################################
    outDFs = monet.initDFsForDA(
        fPaths, header, 
        thi, tho, thw, tap, POE=POE, CPT=CPT
    )[:-1]
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    fmtStr = '{}+ File: {}/{}'
    (i, fPath) = (0, fPaths[0])
    for (i, fPath) in enumerate(fPaths):
        repRto = np.load(fPath)
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND), 
            end='\r'
        )
        #######################################################################
        # Calculate Metrics
        #######################################################################
        mtrsReps = calcMetrics(repRto, thi=thi, tho=tho, thw=thw, tap=tap)
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        mtrsQnt = calcMtrQnts(mtrsReps, qnt)
        #######################################################################
        # Update in Dataframes
        #######################################################################
        (xpid, mtrs) = (
            monet.getXpId(fPath, xpidIx),
            [mtrsQnt[k] for k in DF_SORT]
        )
        updates = [xpid+i for i in mtrs]
        for (df, entry) in zip(outDFs, updates):
            df.iloc[i] = entry
    ###########################################################################
    # Export Data
    ###########################################################################
    for (df, pth) in zip(outDFs, outPaths):
        df.to_csv(pth, index=False)

###############################################################################
# Auxiliary
###############################################################################
def chunks(l, n):
    (d, r) = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield l[si:si+(d+1 if i < r else d)]