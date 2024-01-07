#!/bin/bash

USR=$1
MOS=$2
HUM=$3
QNT='50'
THS=$4
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
METRICS=("CPT" "WOP" "TTI" "TTO")
METRICS_SUM=("CPT" "WOP" "TTI" "TTO")
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Mosquito Scripts
###############################################################################
if [ "$MOS" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${GREEN}[------------MlrProcess------------]${CLEAR}\n"
            for mtr in ${METRICS[*]}; do
                python TPP_mlrTrainKeras.py $USR $lnd $exp "LDR" "HLT" $QNT $THS $mtr
            done
        done
    done
fi
###############################################################################
# Human Scripts
###############################################################################
if [ "$HUM" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${GREEN}[------------MlrProcess------------]${CLEAR}\n"
            for mtr in ${METRICS[*]}; do
                python TPP_mlrTrainKeras.py $USR $lnd $exp "HUM" "PRV" $QNT $THS $mtr
                python TPP_mlrTrainKeras.py $USR $lnd $exp "HUM" "CSS" $QNT $THS $mtr
                python TPP_mlrTrainKeras.py $USR $lnd $exp "HUM" "MRT" $QNT $THS $mtr
            done
        done
    done
fi
