#!/bin/bash

USR=$1
QNT='50'
THS='0.1'
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
METRICS=("WOP" "CPT" "POE" "TTI" "TTO" "MNX")
METRICS_SUM=("WOP" "CPT" "TTI" "TTO" "MNX")
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Mosquito Scripts
###############################################################################
# for lnd in ${LANDS[*]}; do
#     for exp in ${EXPERIMENTS[*]}; do
#         printf "${GREEN}[------------ClsProcess------------]${CLEAR}\n"
#         for mtr in ${METRICS[*]}; do
#             python TPP_clsCompile.py $USR $lnd $exp "LDR" "HLT" $QNT $mtr
#         done
#         python TPP_clsUnify.py $USR $lnd $exp "LDR" "HLT" $QNT $THS
#         printf "${GREEN}[------------DtaProcess------------]${CLEAR}\n"
#         python TPP_dtaExplore.py $USR $lnd $exp "LDR" "HLT" $QNT $THS "HLT"
#         python TPP_dtaTraces.py $USR $lnd $exp "LDR" "HLT" $QNT $THS "HLT"
#     done
# done
###############################################################################
# Human Scripts
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        printf "${GREEN}[------------ClsProcess------------]${CLEAR}\n"
        for mtr in ${METRICS[*]}; do
            python TPP_clsCompile.py $USR $lnd $exp "HUM" "PRV" $QNT $mtr
            python TPP_clsCompile.py $USR $lnd $exp "HUM" "CSS" $QNT $mtr
            python TPP_clsCompile.py $USR $lnd $exp "HUM" "MRT" $QNT $mtr
        done
        python TPP_clsUnify.py $USR $lnd $exp "HUM" "PRV" $QNT $THS
        python TPP_clsUnify.py $USR $lnd $exp "HUM" "CSS" $QNT $THS
        python TPP_clsUnify.py $USR $lnd $exp "HUM" "MRT" $QNT $THS
        printf "${GREEN}[------------DtaExplore------------]${CLEAR}\n"
        python TPP_dtaExplore.py $USR $lnd $exp "HUM" "PRV" $QNT $THS "PRV"
        python TPP_dtaExplore.py $USR $lnd $exp "HUM" "CSS" $QNT $THS "CSS"
        python TPP_dtaExplore.py $USR $lnd $exp "HUM" "MRT" $QNT $THS "MRT"
        printf "${GREEN}[------------DtaTraces-------------]${CLEAR}\n"
        python TPP_dtaTraces.py $USR $lnd $exp "HUM" "PRV" $QNT $THS "PRV"
        python TPP_dtaTraces.py $USR $lnd $exp "HUM" "CSS" $QNT $THS "CSS"
        python TPP_dtaTraces.py $USR $lnd $exp "HUM" "MRT" $QNT $THS "MRT"
    done
done