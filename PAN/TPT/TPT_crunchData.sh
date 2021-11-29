#!/bin/bash

USR=$1

python TPT_preProcess.py $USR 'HUM' 'LDR'
python TPT_preProcess.py $USR 'HLT' 'LDR'
python TPT_pstFraction.py $USR 'HUM' 'LDR'
python TPT_pstFraction.py $USR 'HLT' 'LDR'
