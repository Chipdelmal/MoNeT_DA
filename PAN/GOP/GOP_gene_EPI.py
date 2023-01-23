#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import MoNeT_MGDrivE as monet
import GOP_aux as aux

NH = 182000 # Upper River
NH = 77000  # Brikama
genotypes = (
    "S00_01", "S01_02", "S02_03", "S03_04", "S04_05", "S05_06", "S06_07", "S07_08", "S08_09",
    "T00_01", "T01_02", "T02_03", "T03_04", "T04_05", "T05_06", "T06_07", "T07_08", "T08_09",
    "D00_01", "D01_02", "D02_03", "D03_04", "D04_05", "D05_06", "D06_07", "D07_08", "D08_09",
    "A00_01", "A01_02", "A02_03", "A03_04", "A04_05", "A05_06", "A06_07", "A07_08", "A08_09",
    "U00_01", "U01_02", "U02_03", "U03_04", "U04_05", "U05_06", "U06_07", "U07_08", "U08_09",
    "P00_01", "P01_02", "P02_03", "P03_04", "P04_05", "P05_06", "P06_07", "P07_08", "P08_09",
    
    "ICA00_01", "ICA01_02", "ICA02_03", "ICA03_04", "ICA04_05", "ICA05_06", "ICA06_07", "ICA07_08", "ICA08_09",
    "IB00_01", "IB01_02", "IB02_03", "IB03_04", "IB04_05", "IB05_06", "IB06_07", "IB07_08", "IB08_09",
    "ID00_01", "ID01_02", "ID02_03", "ID03_04", "ID04_05", "ID05_06", "ID06_07", "ID07_08", "ID08_09",
    
    "clin_inc00_01", "clin_inc01_02", "clin_inc02_03", "clin_inc03_04", "clin_inc04_05", 
    "clin_inc05_06", "clin_inc06_07", "clin_inc07_08", "clin_inc08_09",
    
    "mort00_01", "mort01_02", "mort02_03", "mort03_04", "mort04_05", "mort05_06", 
    "mort06_07", "mort07_08", "mort08_09"
)

###############################################################################
#
#   eg: 2-10 age group [00_01, 01_02, 02_03, 03_04]
###############################################################################
# Cases -----------------------------------------------------------------------
stratum = ['00_01', '01_02', '02_03', '03_04']
statDict = {
    'I': ['clin_inc', ], 
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
EPI_CSS = aux.humanGroupsToGeneDict(statDict, stratum, genotypes)
EPI_CSS = {
    'genotypes': list(EPI_CSS.keys()), 
    'indices': list(EPI_CSS.values())
}

# Mortality -------------------------------------------------------------------
stratum = ['00_01', '01_02', '02_03', '03_04']
statDict = {
    'M': ['mort', ], 
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
EPI_MRT = aux.humanGroupsToGeneDict(statDict, stratum, genotypes)
EPI_MRT = {
    'genotypes': list(EPI_MRT.keys()),
    'indices': list(EPI_MRT.values())
}

###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'CSS':
        aggD = EPI_CSS
        yRange = popSize
    elif TYPE == 'MRT':
        aggD = EPI_MRT
        yRange = popSize
    return (aggD, yRange, 'pgSIT')