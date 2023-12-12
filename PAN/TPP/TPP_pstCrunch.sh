#!/bin/bash

USR=$1
MOS=$2
HUM=$3
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
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# PstProcess Mosquito
###############################################################################
if [ "$MOS" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${GREEN}[------------PstFraction------------]${CLEAR}\n"
            python TPP_pstFraction.py $USR $lnd $exp 'LDR' 'HLT'
            python TPP_pstProcess.py $USR $lnd $exp 'LDR' 'HLT' $QNT
        done
    done
fi
###############################################################################
# PstProcess Human
###############################################################################
if [ "$HUM" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${GREEN}[------------PstFraction------------]${CLEAR}\n"
            python TPP_pstFraction.py $USR $lnd $exp 'HUM' 'PRV'
            python TPP_pstFraction.py $USR $lnd $exp 'HUM' 'CSS'
            python TPP_pstFraction.py $USR $lnd $exp 'HUM' 'MRT'
        done
    done
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${GREEN}[------------PstFraction------------]${CLEAR}\n"
            python TPP_pstProcess.py $USR $lnd $exp 'HUM' 'PRV' $QNT
            python TPP_pstProcess.py $USR $lnd $exp 'HUM' 'CSS' $QNT
            python TPP_pstProcess.py $USR $lnd $exp 'HUM' 'MRT' $QNT
        done
    done
fi