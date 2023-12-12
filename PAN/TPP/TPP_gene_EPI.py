#!/usr/bin/python
# -*- coding: utf-8 -*-

import TPP_aux as aux

NH = 182000 # Upper River
NH = 77000  # Brikama
genotypes = (
    'S00_01', 'S01_02', 'S02_03', 'S03_04', 'S04_05', 'S05_06', 'S06_07', 'S07_08', 'S08_09',
    'T00_01', 'T01_02', 'T02_03', 'T03_04', 'T04_05', 'T05_06', 'T06_07', 'T07_08', 'T08_09',
    'D00_01', 'D01_02', 'D02_03', 'D03_04', 'D04_05', 'D05_06', 'D06_07', 'D07_08', 'D08_09',
    'A00_01', 'A01_02', 'A02_03', 'A03_04', 'A04_05', 'A05_06', 'A06_07', 'A07_08', 'A08_09',
    'U00_01', 'U01_02', 'U02_03', 'U03_04', 'U04_05', 'U05_06', 'U06_07', 'U07_08', 'U08_09',
    'P00_01', 'P01_02', 'P02_03', 'P03_04', 'P04_05', 'P05_06', 'P06_07', 'P07_08', 'P08_09', 
    'ICA00_01', 'ICA01_02', 'ICA02_03', 'ICA03_04', 'ICA04_05', 'ICA05_06', 'ICA06_07', 'ICA07_08', 'ICA08_09',
    'IB00_01', 'IB01_02', 'IB02_03', 'IB03_04', 'IB04_05', 'IB05_06', 'IB06_07', 'IB07_08', 'IB08_09',
    'ID00_01', 'ID01_02', 'ID02_03', 'ID03_04', 'ID04_05', 'ID05_06', 'ID06_07', 'ID07_08', 'ID08_09',
    'IVA00_01', 'IVA01_02', 'IVA02_03', 'IVA03_04', 'IVA04_05', 'IVA05_06', 'IVA06_07', 'IVA07_08', 'IVA08_09',
    'clin_inc00_01', 'clin_inc01_02', 'clin_inc02_03', 'clin_inc03_04', 'clin_inc04_05', 'clin_inc05_06', 'clin_inc06_07', 'clin_inc07_08', 'clin_inc08_09',
    'mort00_01', 'mort01_02', 'mort02_03', 'mort03_04', 'mort04_05', 'mort05_06', 'mort06_07', 'mort07_08', 'mort08_09'
)

AGE_GROUP_LABEL = ['0 to 5', '5 to 17', '17 to 40', '40 to 60', '60 and older'] #, '99 and older']
###############################################################################
# Dictionaries
###############################################################################
strata = [['00_01', '01_02', '02_03', '03_04', '04_05', '05_06', '06_07', '07_08', '08_09']]
# Incidence -------------------------------------------------------------------
statDict = {
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'I': ['clin_inc', ] 
    # 'T': ['clin_inc', ] # ['S', 'T', 'D', 'A', 'U', 'P']
}
EPI_CSS_FULL = []
for st in strata:
    EPI_CSS = aux.humanGroupsToGeneDict(statDict, st, genotypes)
    EPI_CSS = {
        'genotypes': list(EPI_CSS.keys()),
        'indices': list(EPI_CSS.values())
    }
    EPI_CSS_FULL.append(EPI_CSS)
# Mortality -------------------------------------------------------------------
statDict = { 
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'M': ['mort', ]
    # 'T': ['mort', ] # ['S', 'T', 'D', 'A', 'U', 'P']
}
EPI_MRT_FULL = []
for st in strata:
    EPI_MRT = aux.humanGroupsToGeneDict(statDict, st, genotypes)
    EPI_MRT = {
        'genotypes': list(EPI_MRT.keys()),
        'indices': list(EPI_MRT.values())
    }
    EPI_MRT_FULL.append(EPI_MRT)
# Prevalence ------------------------------------------------------------------
statDict = {
    'P': ['T', 'D', 'A', 'U'], 
    'O': ['S', 'P'],
    # 'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
EPI_PRV_FULL = []
for st in strata:
    EPI_PRV = aux.humanGroupsToGeneDict(statDict, st, genotypes)
    EPI_PRV = {
        'genotypes': list(EPI_PRV.keys()),
        'indices': list(EPI_PRV.values())
    }
    EPI_PRV_FULL.append(EPI_PRV)
###############################################################################
# Drive Selector
###############################################################################
def driveParameters(TYPE, popSize):
    if TYPE == 'CSS': (yRange, aggD) = (1250, EPI_MRT_FULL[0])
    elif TYPE == 'MRT': (yRange, aggD) = (1250, EPI_CSS_FULL[0])
    elif TYPE == 'PRV': (yRange, aggD) = (1250, EPI_PRV_FULL[0])
    return (aggD, yRange, 'pgSIT')
