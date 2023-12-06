#!/usr/bin/python
# -*- coding: utf-8 -*-

import TPP_aux as aux

NH = 182000 # Upper River
NH = 77000  # Brikama
genotypes = (
    'S00_01', 'S01_02', 'S02_03', 'S03_04', 'S04_05', 'S05_06', 
    'T00_01', 'T01_02', 'T02_03', 'T03_04', 'T04_05', 'T05_06', 
    'D00_01', 'D01_02', 'D02_03', 'D03_04', 'D04_05', 'D05_06', 
    'A00_01', 'A01_02', 'A02_03', 'A03_04', 'A04_05', 'A05_06', 
    'U00_01', 'U01_02', 'U02_03', 'U03_04', 'U04_05', 'U05_06', 
    'P00_01', 'P01_02', 'P02_03', 'P03_04', 'P04_05', 'P05_06', 
    
    'ICA00_01', 'ICA01_02', 'ICA02_03', 'ICA03_04', 'ICA04_05', 'ICA05_06', 
    'IB00_01', 'IB01_02', 'IB02_03', 'IB03_04', 'IB04_05', 'IB05_06', 
    'ID00_01', 'ID01_02', 'ID02_03', 'ID03_04', 'ID04_05', 'ID05_06', 
    'IVA00_01', 'IVA01_02', 'IVA02_03', 'IVA03_04', 'IVA04_05', 'IVA05_06', 
    
    'clin_inc00_01', 'clin_inc01_02', 'clin_inc02_03', 'clin_inc03_04', 'clin_inc04_05', 'clin_inc05_06', 
    
    'mort00_01', 'mort01_02', 'mort02_03', 'mort03_04', 'mort04_05', 'mort05_06'
)

AGE_GROUP_LABEL = ['0 to 5', '5 to 17', '17 to 40', '40 to 60', '60 and older'] #, '99 and older']
###############################################################################
# Dictionaries
###############################################################################
# Incidence -------------------------------------------------------------------
statDict = {
    'I': ['clin_inc', ], 
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
strata = [['00_01', '01_02', '02_03', '03_04', '04_05', '05_06']]
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
    'M': ['mort', ], 
    'O': ['S', 'T', 'D', 'A', 'U', 'P'],
    'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
strata = [['00_01', '01_02', '02_03', '03_04', '04_05', '05_06']]
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
    'M': ['T', 'D', 'A', 'U'], 
    'O': ['S', 'P'],
    'T': ['S', 'T', 'D', 'A', 'U', 'P']
}
strata = [['00_01', '01_02', '02_03', '03_04', '04_05', '05_06']]
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
