#!/bin/bash

USR=$1
###############################################################################
# Constants
###############################################################################
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
RED='\033[0;31m'
WHITE='\033[0;37m'
LANDS=("BurkinaFaso" "Kenya")
EXPERIMENTS=("highEIR" "medEIR" "lowEIR")
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# PreProcess
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        printf "${GREEN}[------------PreProcess------------]${CLEAR}\n"
        python TPP_preProcess.py $USR $lnd $exp 'LDR' 'ECO'
        python TPP_preProcess.py $USR $lnd $exp 'LDR' 'HLT'
    done
done
###############################################################################
# PreTraces
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        printf "${GREEN}[------------PreTraces------------]${CLEAR}\n"
        python TPP_preTraces.py $USR $lnd $exp 'LDR' 'ECO'
        python TPP_preTraces.py $USR $lnd $exp 'LDR' 'HLT'
    done
done