
import numpy as np
import pandas as pd
from os import path
import compress_pickle as pkl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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


def exportPstTracesPlotWrapper(
        exIx, repFiles, xpidIx, 
        dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT,
        STABLE_T, THS, QNT, STYLE, PT_IMG, 
        border=True, borderColor='#322E2D', borderWidth=1, 
        labelPos=(.75, .95), xpsNum=0, digs=3, 
        autoAspect=False, popScaler=1,
        wopPrint=True, cptPrint=True, 
        poePrint=True, mnfPrint=True,
        transparent=False, 
        ticksHide=True, sampRate=1,
        fontsize=5, labelspacing=.1, 
        vlines=[], hlines=[]
    ):
    padi = str(exIx+1).zfill(digs)
    fmtStr = '{}+ File: {}/{}'
    print(fmtStr.format(monet.CBBL, padi, len(repFiles), monet.CEND), end='\r')
    repFile = repFiles[exIx]
    (repDta, xpid) = (
            pkl.load(repFile), monet.getXpId(repFile, xpidIx)
        )
    xpRow = [
        monet.filterDFWithID(j, xpid, max=len(xpidIx)) for j in (
            dfTTI, dfTTO, dfWOP, dfMNX, dfPOE, dfCPT
        )
    ]
    (tti, tto, wop) = [float(row[THS]) for row in xpRow[:3]]
    (mnf, mnd, poe, cpt) = (
        float(xpRow[3]['min']), float(xpRow[3]['minx']), 
        float(xpRow[4]['POE']), float(xpRow[5]['CPT'])
    )
    # Traces ------------------------------------------------------------------
    pop = repDta['landscapes'][0][STABLE_T][-1]
    # STYLE['yRange'] = (0,  pop*popScaler)
    exportTracesPlot(
        repDta, repFile.split('/')[-1][:-6]+str(QNT), STYLE, PT_IMG,
        vLines=[tti, tto, 0]+vlines, hLines=[0]+hlines, labelPos=labelPos, 
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        autoAspect=autoAspect, popScaler=popScaler,
        wop=wop, wopPrint=wopPrint, 
        cpt=cpt, cptPrint=cptPrint,
        poe=poe, poePrint=poePrint,
        mnf=mnf, mnfPrint=mnfPrint,
        transparent=transparent, ticksHide=ticksHide, sampRate=sampRate,
        fontsize=fontsize, labelspacing=labelspacing
    )
    return None


def exportTracesPlot(
    tS, nS, STYLE, PATH_IMG, append='', 
    vLines=[0, 0], hLines=[0], labelPos=(.7, .95), autoAspect=False,
    border=True, borderColor='#8184a7AA', borderWidth=2, popScaler=1,
    wop=0, wopPrint=True, 
    cpt=0, cptPrint=False, 
    poe=0, poePrint=False,
    mnf=0, mnfPrint=False,
    transparent=False, ticksHide=True, sampRate=1,
    fontsize=5, labelspacing=.1
):
    # print(STYLE['xRange'][0])
    if transparent:
        plt.rcParams.update({
            "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),
            "axes.facecolor":    (0.0, 1.0, 0.0, 0.0),
            "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),
        })
    figArr = monet.plotNodeTraces(tS, STYLE, sampRate=sampRate)
    axTemp = figArr[0].get_axes()[0]
    STYLE['yRange'] = (STYLE['yRange'][0], STYLE['yRange'][1]*popScaler)
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    axTemp.set_ylim(STYLE['yRange'][0], STYLE['yRange'][1])
    if autoAspect:
        axTemp.set_aspect(aspect=monet.scaleAspect(STYLE["aspect"], STYLE))
    else:
        axTemp.set_aspect(aspect=STYLE["aspect"])
    if ticksHide:
        axTemp.axes.xaxis.set_ticklabels([])
        axTemp.axes.yaxis.set_ticklabels([])
        axTemp.axes.xaxis.set_visible(False)
        axTemp.axes.yaxis.set_visible(False)
        # axTemp.xaxis.set_tick_params(width=0)
        # axTemp.yaxis.set_tick_params(width=0)
        axTemp.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        axTemp.set_axis_off()
    axTemp.xaxis.set_ticks(np.arange(STYLE['xRange'][0], STYLE['xRange'][1], 365))
    axTemp.yaxis.set_ticks(np.arange(STYLE['yRange'][0], STYLE['yRange'][1], STYLE['yRange'][1]/4))
    axTemp.grid(which='major', axis='y', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))
    axTemp.grid(which='major', axis='x', lw=.5, ls='-', alpha=0.0, color=(0, 0, 0))

    days = tS['landscapes'][0].shape[0]*sampRate
    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] < vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#3687ff', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-', lw=.1, color='#3687ff', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-', lw=.1, color='#3687ff', zorder=0)

    if (vLines[0] > 0) and (vLines[1] <= days) and (wop > 0) and (vLines[0] > vLines[1]):
        axTemp.axvspan(vLines[0], vLines[1], alpha=0.15, facecolor='#FF5277', zorder=0)
        axTemp.axvline(vLines[0], alpha=0.75, ls='-', lw=.1, color='#FF1A4B', zorder=0)
        axTemp.axvline(vLines[1], alpha=0.75, ls='-', lw=.1, color='#FF1A4B', zorder=0)

    for hline in hLines:
        axTemp.axhline(hline, alpha=.25, zorder=10, ls='-', lw=.2, color='#000000')
    for vline in vLines[2:]:
        axTemp.axvline(vline, alpha=.25, zorder=10, ls='-', lw=.2, color='#000000')
    # Print metrics -----------------------------------------------------------
    if  wopPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*0, 'WOP: '+str(int(wop)),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )
    if cptPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*1, 'CPT: {:.3f}'.format(cpt),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )         
    if mnfPrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*2, 'MIN: {:.3f}'.format(mnf),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        )     
    if poePrint:
        axTemp.text(
            labelPos[0], labelPos[1]-labelspacing*3, 'POE: {:.3f}'.format(poe),
            verticalalignment='bottom', horizontalalignment='left',
            transform=axTemp.transAxes,
            color='#00000055', fontsize=fontsize
        ) 
    # --------------------------------------------------------------------------
    #axTemp.tick_params(color=(0, 0, 0, 0.5))
    # extent = axTemp.get_tightbbox(figArr[0]).transformed(figArr[0].dpi_scale_trans.inverted())
    if border:
        axTemp.set_axis_on()
        plt.setp(axTemp.spines.values(), color=borderColor)
        pad = 0.025
        for axis in ['top','bottom','left','right']:
            axTemp.spines[axis].set_linewidth(borderWidth)
    else:
        pad = 0
    axTemp.set_xlim(STYLE['xRange'][0], STYLE['xRange'][1])
    figArr[0].savefig(
            "{}/{}.png".format(PATH_IMG, nS),
            dpi=STYLE['dpi'], facecolor=None,
            orientation='portrait', format='png', 
            transparent=transparent, bbox_inches='tight', pad_inches=pad
        )
    plt.clf()
    plt.cla() 
    plt.close('all')
    plt.gcf()
    return None


def exportPreTracesParallel(
            exIx, STYLE, PT_IMG,
            border=True, borderColor='#322E2D', borderWidth=1, autoAspect=False,
            xpNum=0, digs=3, vLines=[0, 0], hLines=[0], popScaler=1,
            transparent=True, sampRate=1
        ):
    monet.printProgress(exIx[0], xpNum, digs)
    repFilePath = exIx[1][1]
    repDta = pkl.load(repFilePath)
    name = path.splitext(repFilePath.split('/')[-1])[0][:-4]
    exportTracesPlot(
        repDta, name, STYLE, PT_IMG, wopPrint=False, autoAspect=autoAspect,
        border=border, borderColor=borderColor, borderWidth=borderWidth,
        vLines=vLines, transparent=transparent, sampRate=sampRate
    )
    return None