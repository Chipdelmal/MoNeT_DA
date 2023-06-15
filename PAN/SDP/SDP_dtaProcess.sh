#!/bin/bash

# argv1: USR
# argv2: DRV

USR=$1
DRV=$2
AOI=$3
QNT=$4
THS=$5

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Run Scripts
###############################################################################
for mtr in "WOP" "CPT" "POE" "TTI" "TTO" "MNX"
do
    python SDP_dtaCompile.py $USR $DRV $AOI $QNT $mtr
done
python SDP_dtaUnify.py $USR $DRV $AOI $QNT $THS