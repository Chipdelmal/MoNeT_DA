#!/bin/bash

USR=$1

python TPT_preProcess.py $USR 'HUM' 'LDR'
python TPT_preProcess.py $USR 'HLT' 'LDR'