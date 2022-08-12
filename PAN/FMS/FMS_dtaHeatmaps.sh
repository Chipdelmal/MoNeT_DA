#!/bin/bash

USR=$1
DRV=$2
QNT=$3
AOI=$4
THS=$5

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for drv in "FMS3" "FMS4" "FMS5" "PGS"
do
    for mtr in "WOP" "CPT" "POE" "TTI"
    do
        python FMS_dtaHeatmap.py $USR $drv $QNT $AOI $THS $mtr
    done
done