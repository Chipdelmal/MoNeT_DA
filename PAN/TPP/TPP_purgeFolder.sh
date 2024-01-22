#!/bin/bash

USR=$1
HTM=$2

# BASE_PATH="/Users/sanchez.hmsc/Documents/WorkSims/TPP"
# BASE_PATH = '/RAID5/marshallShare/ReplacementTPP/'
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
            for ths in ${THRESHOLDS[*]};do
                printf "${RED}* Heatmaps: ${CLEAR}${BLUE}${lnd} - ${exp}:ML${ths}${CLEAR}\n"
                if [ "$USR" == "zelda" ]; then
                    rm /RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML${ths}/img/heatmaps/*.png
                fi
                if [ "$USR" == "lap" ]; then
                    FPTH="/Users/sanchez.hmsc/Documents/WorkSims/TPP/${lnd}/${exp}/ML${ths}/img/heatmaps/"
                    find $FPTH -name "*.png" -delete
                fi
            done
        done
    done
fi



# "/Users/sanchez.hmsc/Documents/WorkSims/TPP/BurkinaFaso/highEIR/ML25/img/heatmaps"