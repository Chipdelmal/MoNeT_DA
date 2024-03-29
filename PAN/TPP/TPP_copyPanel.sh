#!/bin/bash

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
BASE_FILE="/Users/sanchez.hmsc/Documents/WorkSims/TPP/BurkinaFaso/highEIR/ML25/img/heatmaps/PanelMix.svg"
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        printf "${RED}* Copying: ${CLEAR}${BLUE}${lnd} - ${exp}${CLEAR}\n"
        for ths in ${THRESHOLDS[*]};do
            FPTH="/Users/sanchez.hmsc/Documents/WorkSims/TPP/${lnd}/${exp}/ML${ths}/img/heatmaps/"
            cp -f $BASE_FILE $FPTH
            /Applications/Inkscape.app/Contents/MacOS/inkscape "${FPTH}/PanelMix.svg" --export-filename="${FPTH}/PanelMix-Auto.png" -b "white"
        done
    done
done