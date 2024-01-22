#!/bin/bash

MLR=$1
HTM=$2
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
THRESHOLDS=("25" "33" "50")
###############################################################################
# ML Download Loop
###############################################################################
if [ "$MLR" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        mkdir -p "${BASE_PATH}/${lnd}"
        for exp in ${EXPERIMENTS[*]}; do
            printf "${RED}* ML Regression: ${CLEAR}${BLUE}${lnd} - ${exp}${CLEAR}\n"
            mkdir -p "${BASE_PATH}/${lnd}/${exp}/"
            scp -q -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/img/dtaTraces[0-9][0-9]/" "${BASE_PATH}/${lnd}/${exp}/img/"
            # scp -q -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML*/" "${BASE_PATH}/${lnd}/${exp}/"
            # scp -q -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/SUMMARY/" "${BASE_PATH}/${lnd}/${exp}/"
        done
    done
fi
###############################################################################
# Heatmap Download Loop
#   scp zelda:"/RAID5/marshallShare/ReplacementTPP/BurkinaFaso/highEIR/ML25/img/heatmaps/*WOP*.png" "/Users/sanchez.hmsc/Documents/WorkSims/TPP/BurkinaFaso/highEIR/ML25/img/heatmaps"
###############################################################################
if [ "$HTM" == "True" ]; then
    for lnd in ${LANDS[*]}; do
        for exp in ${EXPERIMENTS[*]}; do
            printf "${RED}* Heatmaps: ${CLEAR}${BLUE}${lnd} - ${exp}${CLEAR}\n"
            for ths in ${THRESHOLDS};do
                mkdir -p "${BASE_PATH}/${lnd}/${exp}/ML${ths}/img/heatmaps/"
                scp -q -r zelda:"/RAID5/marshallShare/ReplacementTPP/${lnd}/${exp}/ML${ths}/img/heatmaps/*ALT*.png" "${BASE_PATH}/${lnd}/${exp}/ML${ths}/img/heatmaps/"
            done
        done
    done
fi
