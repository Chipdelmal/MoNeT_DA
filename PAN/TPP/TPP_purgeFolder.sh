#!/bin/bash

HTM=$1

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
THRESHOLDS=("25" "33" "50")
###############################################################################
# Purge Loop
###############################################################################
if [ "$HTM" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${RED}* Heatmaps: ${CLEAR}${BLUE}${lnd} - ${exp}${CLEAR}\n"
            for ths in ${THRESHOLDS};do
                rm "/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML${ths}/img/heatmaps/*.png"
            done
        done
    done
fi
