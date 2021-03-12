
import numpy as np
import pandas as pd


def unifySexesDataframe(dfRC, EXPS, FEATS, LBLS):
    df = pd.DataFrame(columns=['i_sex']+FEATS+LBLS)
    for i in range(len(EXPS)):
        dfTemp = dfRC[EXPS[i]]
        for j in range(dfTemp.shape[0]):
            row = dict(dfTemp.iloc[j])
            row['i_sex'] = EXPS[i]
            df = df.append(row, ignore_index=True)
    return df


def rescaleDataset(df, SCA=1):
    df['i_rer'] = df['i_rer'] / SCA
    df['i_ren'] = df['i_ren']
    df['i_rsg'] = df['i_rsg'] / SCA
    df['i_fic'] = df['i_fic'] / SCA
    df['i_gsv'] = df['i_gsv'] / SCA
    df['i_grp'] = df['i_grp']
    return df


def getBoolIxFromFeatKey(df, key, FEATS):
    matches = [list(np.isclose(df[feat], key[feat])) for feat in FEATS]
    ixBool = [all(row) for row in list(zip(*matches))]
    return ixBool


def zeroDivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def dividePops(n, d):
    return (n / d if d else 0)


def errorBetweenDataframes(dfB, dfP, FEATS, LABELS, error=True):
    dfO = dfB.copy()
    for i in range(dfB.shape[0]):
        sliceKey = dfB.iloc[i][FEATS]
        outB = dfB.iloc[i][LABELS].values
        boolFltr = getBoolIxFromFeatKey(dfP, sliceKey, FEATS)
        outP = dfP[boolFltr][LABELS].values
        if error:
            diff = zeroDivide(outP, outB)
        else:
            diff = zeroDivide(outP - outB, 1)
        dfO.iloc[boolFltr.index(True)] = list(sliceKey) + list(diff[0])
    return dfO


def geneCountsToFractions(popCountsArray):
    totalPop = popCountsArray[:, -1]
    geneFractions = [
        zeroDivide(popCountsArray[:, i], totalPop) 
        for i in range(len(popCountsArray[0])-1)
    ]
    geneFractions.append(totalPop)
    return np.asarray(geneFractions).T


def aggCentroids(AGG_lonlats):
    centroids = [(np.mean(i[:, 0]), np.mean(i[:, 1])) for i in AGG_lonlats]
    return np.asarray(centroids)




def initDFsForDA(
            fPaths, header, thiS, thoS, thwS, ttpS,
            peak=['min', 'minx', 'max', 'maxx'],
            POE=False, poe=['POE', 'POF'],
            CPT=False, cpt=['CPT']
        ):
    fNum = len(fPaths)
    if (POE and not CPT):
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, poe)]
    elif (CPT and not POE): 
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, cpt)]
    elif (POE and CPT):
        heads = [
            list(header)+i for i in (thiS, thoS, thwS, ttpS, peak, poe, cpt)
        ]
    else:
        heads = [list(header)+i for i in (thiS, thoS, thwS, ttpS, peak)]
    DFEmpty = [pd.DataFrame(int(0), index=range(fNum), columns=h) for h in heads]
    return DFEmpty


def calcPOE(repRto, finalDay=-1, thresholds=(.025, .975)):
    (reps, days) = repRto.shape
    if finalDay == -1:
        fD = -1
    else:
        fD = finalDay
    fR = [rep[fD] for rep in repRto]
    (loTh, hiTh) = (
        [j < thresholds[0] for j in fR],
        [j > thresholds[1] for j in fR]
    )
    (pLo, pHi) = (sum(loTh)/reps, sum(hiTh)/reps)
    return (pLo, pHi)


def calcCPT(repRto):
    return [np.sum(i)/repRto.shape[1] for i in repRto]