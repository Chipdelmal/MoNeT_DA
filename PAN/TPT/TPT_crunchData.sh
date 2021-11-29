#!/bin/bash

USR=$1
QNT='50'

# PreProcess ------------------------------------------------------------------
python TPT_preProcess.py $USR 'HUM' 'LDR'
python TPT_preProcess.py $USR 'HLT' 'LDR'
# PstFraction -----------------------------------------------------------------
python TPT_pstFraction.py $USR 'HUM' 'LDR'
python TPT_pstFraction.py $USR 'HLT' 'LDR'
# PstProcess ------------------------------------------------------------------
python TPT_pstProcess.py $USR 'HUM' 'LDR' $QNT
python TPT_pstProcess.py $USR 'HLT' 'LDR' $QNT
