#!/bin/bash

###############################################################################
# Constants
###############################################################################
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
RED='\033[0;31m'
WHITE='\033[0;37m'
# -----------------------------------------------------------------------------
LANDS=("BurkinaFaso")
EXPERIMENTS=("highEIR")
###############################################################################
# ML Download Loop
###############################################################################
for lnd in ${LANDS[*]}; do
    for exp in ${EXPERIMENTS[*]}; do
        scp -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML/" "/Users/sanchez.hmsc/Documents/WorkSims/TPP/${lnd}/${exp}/"
    done
done