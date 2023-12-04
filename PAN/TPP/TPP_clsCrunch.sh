#!/bin/bash

USR=$1
QNT='50'
###############################################################################
# Constants
###############################################################################
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
RED='\033[0;31m'
WHITE='\033[0;37m'
# -----------------------------------------------------------------------------
LANDS=("BurkinaFaso" "Kenya")
EXPERIMENTS=("highEIR" "medEIR" "lowEIR")
METRICS=("WOP" "CPT" "TTI" "TTO" "MNX")
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        for mtr in ${METRICS[*]}; do
            python TPP_clsCompile.py $USR $lnd $exp "LDR" "HLT" $QNT $mtr
        done
    done
done
# python PGS_clsUnify.py $USR $DRV $QNT $AOI $THS 
# python PGS_dtaExplore.py $USR $DRV $QNT $AOI $THS $AOI
# python PGS_dtaTraces.py $USR $DRV $QNT $AOI