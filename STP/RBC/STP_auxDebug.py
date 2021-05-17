
import numpy as np
import compress_pickle as pkl
import MoNeT_MGDrivE as monet

def preProcessLandscape(
            pathMean, pathTraces, expName, drive, prePath='./',
            nodesAggLst=[[0]], analysisOI='HLT', fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True,
            sexFilenameIdentifiers={"male": "M_", "female": "F_"}
        ):
    dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
    files = monet.readExperimentFilenames(
        pathMean, sexFilenameIdentifiers=sexFilenameIdentifiers
    )
    filesList = [monet.filterFilesByIndex(files, ix) for ix in nodesAggLst]
    landReps = None
    if REP or SRP:
        landReps = monet.loadAndAggregateLandscapeDataRepetitions(
                dirsTraces, drive, MF[0], MF[1],
                sexFilenameIdentifiers=sexFilenameIdentifiers
            )
    for (nodeAggIx, pop) in enumerate(filesList):
        fName = fNameFmt + str(nodeAggIx).zfill(nodeDigits)
        monet.preProcessSubLandscape(
                    pop, landReps, fName, drive,
                    nodesAggLst, nodeAggIx,
                    MF=MF, cmpr=cmpr,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
                )
    # return None


def preProcessParallel(
            exIx, expNum, expDirsMean, expDirsTrac,
            drive, analysisOI='HLT', prePath='./',
            nodesAggLst=[[0]], fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=False, SPA=False, REP=False, SRP=True,
            sexFilenameIdentifiers={"male": "M_", "female": "F_"}
        ):
    monet.printProgress(exIx+1, expNum, nodeDigits)
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx]+'/')
    expName = pathMean.split('/')[-1]
    fNameFmt = '{}/{}-{}_'.format(prePath, expName, analysisOI)
    preProcessLandscape(
        pathMean, pathTraces, expName, drive, prePath,
        analysisOI=analysisOI, nodesAggLst=nodesAggLst,
        fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers=sexFilenameIdentifiers
    )
    # return None


def pstFractionParallel(
        pIx, PT_OUT,
        baseFiles, meanFiles, traceFiles
    ):
    # Load data ---------------------------------------------------------------
    (bFile, mFile, tFile) = (baseFiles[pIx], meanFiles[pIx], traceFiles[pIx])
    (base, mean, trace) = [pkl.load(file) for file in (bFile, mFile, tFile)]
    # Process data ------------------------------------------------------------
    fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
    repsRatios = monet.getPopRepsRatios(base, trace, 1)
    np.save(fName, repsRatios)