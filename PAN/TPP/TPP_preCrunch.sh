#!/bin/bash

USR=$1
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for lnd in "Kenya"
    for exp in "highEIR"  "lowEIR"  "medEIR"
    do
        python TPP_preProcess.py $USR $lnd $exp 'LDR' 'ECO'
        python TPP_preProcess.py $USR $lnd $exp 'LDR' 'HLT'
    done
done