#!/bin/bash

USR=$1
QNT='50'
THS='0.1'

# PreProcess ------------------------------------------------------------------
# python TPT_preProcess.py $USR 'HUM' 'LDR'
# python TPT_preProcess.py $USR 'HLT' 'LDR'
# python TPT_preProcess.py $USR 'ECO' 'LDR'
# python TPT_preTraces.py $USR 'HUM' 'LDR'
# python TPT_preTraces.py $USR 'HLT' 'LDR'
# python TPT_preTraces.py $USR 'ECO' 'LDR'
# python TPT_preTracesInfectious.py $USR 'HLT' 'LDR'
# PstFraction -----------------------------------------------------------------
# python TPT_pstFraction.py $USR 'HUM' 'LDR'
# python TPT_pstFraction.py $USR 'HLT' 'LDR'
# PstProcess ------------------------------------------------------------------
# python TPT_pstProcess.py $USR 'HUM' 'LDR' $QNT
# python TPT_pstProcess.py $USR 'HLT' 'LDR' $QNT
python TPT_pstTraces.py $USR 'HLT' 'LDR' $QNT $THS
python TPT_pstTraces.py $USR 'HUM' 'LDR' $QNT $THS
