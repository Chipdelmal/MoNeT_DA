#!/bin/bash

BASE_PATH="/Users/sanchez.hmsc/Documents/WorkSims/TPP"
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
# ML Download Loop
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        printf "${BLUE}${lnd} - ${exp}${CLEAR}\n"
        scp -q -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML/" "${BASE_PATH}/${lnd}/${exp}/"
    done
done