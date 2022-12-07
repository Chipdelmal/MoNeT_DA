#!/bin/bash

USR=$1 # 'lab' or 'srv'
QNT='50'
THS='0.1'
SPE=$2 # 'gambiae' or 'coluzii'

# # Data Fixes ------------------------------------------------------------------
# python TPT_incidenceFix.py $USR 'INC' 'LDR' $SPE
# # PreProcess ------------------------------------------------------------------
# python TPT_preProcess.py $USR 'HUM' 'LDR' $SPE
# python TPT_preProcess.py $USR 'HLT' 'LDR' $SPE
# python TPT_preProcess.py $USR 'ECO' 'LDR' $SPE
# python TPT_preProcess.py $USR 'INC' 'LDR' $SPE
# PreTraces ------------------------------------------------------------------
python TPT_preTraces.py $USR 'HUM' 'LDR' $SPE
python TPT_preTraces.py $USR 'HLT' 'LDR' $SPE
python TPT_preTraces.py $USR 'ECO' 'LDR' $SPE
python TPT_preTraces.py $USR 'INC' 'LDR' $SPE
# # PstFraction -----------------------------------------------------------------
# python TPT_pstFraction.py $USR 'HUM' 'LDR' $SPE
# python TPT_pstFraction.py $USR 'HLT' 'LDR' $SPE
# python TPT_pstFraction.py $USR 'INC' 'LDR' $SPE
# # PstProcess ------------------------------------------------------------------
# python TPT_pstProcess.py $USR 'HUM' 'LDR' $QNT $SPE
# python TPT_pstProcess.py $USR 'HLT' 'LDR' $QNT $SPE
# python TPT_pstProcess.py $USR 'INC' 'LDR' $QNT $SPE
python TPT_pstTraces.py $USR 'HUM' 'LDR' $QNT $THS $SPE
python TPT_pstTraces.py $USR 'HLT' 'LDR' $QNT $THS $SPE
python TPT_pstTraces.py $USR 'INC' 'LDR' $QNT $THS $SPE