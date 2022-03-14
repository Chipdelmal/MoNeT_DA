
import MoNeT_MGDrivE as monet


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
    preProcessLandscape(
        pathMean, pathTraces, expName, drive, prePath,
        analysisOI=analysisOI, nodesAggLst=nodesAggLst,
        fNameFmt=fNameFmt, MF=MF, cmpr=cmpr, nodeDigits=nodeDigits,
        SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
        sexFilenameIdentifiers=sexFilenameIdentifiers
    )
    return None


def preProcessLandscape(
            pathMean, pathTraces, expName, drive, prePath='./',
            nodesAggLst=[[0]], analysisOI='HLT', fNameFmt='{}/{}-{}_',
            MF=(True, True), cmpr='bz2', nodeDigits=4,
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True,
            sexFilenameIdentifiers={"male": "M_", "female": "F_"}
        ):
    dirsTraces = monet.listDirectoriesWithPathWithinAPath(pathTraces)
    files = readExperimentFilenames(
        pathMean, sexFilenameIdentifiers=sexFilenameIdentifiers
    )
    filesList = [monet.filterFilesByIndex(files, ix) for ix in nodesAggLst]
    landReps = None
    if REP or SRP:
        landReps = loadAndAggregateLandscapeDataRepetitions(
                dirsTraces, drive, MF[0], MF[1],
                sexFilenameIdentifiers=sexFilenameIdentifiers
            )
    # for (nodeAggIx, pop) in enumerate(filesList):
    #     fName = fNameFmt + str(nodeAggIx).zfill(nodeDigits)
    #     preProcessSubLandscape(
    #                 pop, landReps, fName, drive,
    #                 nodesAggLst, nodeAggIx,
    #                 MF=MF, cmpr=cmpr,
    #                 SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP,
    #             )
    return None


def loadAndAggregateLandscapeDataRepetitions(
    paths,
    aggregationDictionary,
    male=True,
    female=True,
    dataType=float,
    sexFilenameIdentifiers={"male": "M_", "female": "F_"}
):
    """
    Description:
        * Loads and aggregates the genotypes of the landscape accross
            repetitions of the same experiment.
    In:
        * paths: Repetitions folders locations.
        * aggregationDictionary: Genotypes and indices counts dictionary.
        * male: Boolean to select male files for the aggregation.
        * female: Boolean to select female files for the aggregation.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * returnDict: Dictionary with genotypes and the loaded landscapes
            for each one of the repetitions.
    Notes:
        * This function is meant to work with the traces plot, so it has a
            higher dimension (repetitions) than regular spatial analysis
            versions.
    """
    pathsNumber = len(paths)
    landscapes = [None] * pathsNumber
    print(aggregationDictionary)
    for i in range(0, pathsNumber):
        filenames = readExperimentFilenames(
            paths[i], sexFilenameIdentifiers=sexFilenameIdentifiers
        )
        loadedLandscape = monet.loadAndAggregateLandscapeData(
            filenames, aggregationDictionary,
            male=male, female=female, dataType=dataType
        )
        landscapes[i] = loadedLandscape["landscape"]
    returnDict = {
        "genotypes": aggregationDictionary["genotypes"],
        "landscapes": landscapes
    }
    return returnDict


def preProcessSubLandscape(
            pop, landReps, fName, drive,
            nodesAggLst, nodeAggIx,
            MF=(True, True), cmpr='bz2',
            SUM=True, AGG=True, SPA=True, REP=True, SRP=True
        ):
    if SUM:
        sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
        print(sumData)
        sumAgg = exp.aggregateGenotypesInNode(sumData, drive)
        pkl.dump(sumAgg, fName+'_sum', compression=cmpr)
    if AGG:
        aggData = monet.loadAndAggregateLandscapeData(pop, drive, MF[0], MF[1])
        pkl.dump(aggData, fName+'_agg', compression=cmpr)
    if SPA:
        geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
        pkl.dump(geneSpaTemp, fName+'_spa', compression=cmpr)
    if REP or SRP:
        fLandReps = monet.filterAggregateGarbageByIndex(
                landReps, nodesAggLst[nodeAggIx]
            )
        if REP:
            pkl.dump(fLandReps, fName+'_rep', compression=cmpr)
    if SRP:
        fRepsSum = [sum(i) for i in fLandReps['landscapes']]
        fRepsDict = {
                'genotypes': fLandReps['genotypes'],
                'landscapes': fRepsSum
            }
        pkl.dump(fRepsDict, fName+'_srp', compression=cmpr)
    return None


def readExperimentFilenames(
    experimentPath,
    sexFilenameIdentifiers={"male": "", "female": ""},
    exclusionPattern=None
):
    defaultIdentifiers = {"male": ["M_", "ADM"], "female": ["F_", "AF1"]}

    maleFiles = []
    if 'male' in sexFilenameIdentifiers:
        maleFiles = monet.getFileExperimentList(
                experimentPath, sexFilenameIdentifiers['male']
            )
        if not maleFiles:
            for i in defaultIdentifiers['male']:
                fileList = monet.getFileExperimentList(experimentPath, i)
                if fileList:
                    maleFiles = fileList
                    break

    femaleFiles = []
    if 'female' in sexFilenameIdentifiers:
        femaleFiles = monet.getFileExperimentList(
                experimentPath, sexFilenameIdentifiers['female']
            )
        if not femaleFiles:
            for i in defaultIdentifiers['female']:
                fileList = monet.getFileExperimentList(experimentPath, i)
                if fileList:
                    femaleFiles = fileList
                    break


    if exclusionPattern is not None:
        maleFiles = [i for i in maleFiles if exclusionPattern(i)]
        femaleFiles = [i for i in femaleFiles if exclusionPattern(i)]

    return {"male": maleFiles, "female": femaleFiles}


