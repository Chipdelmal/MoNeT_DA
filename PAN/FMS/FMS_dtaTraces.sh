#!/bin/bash

USR=$1
DRV=$2
QNT=$3
AOI=$4
THS=$5
TRC=$6

# ./FMS_dtaTraces.sh srv FMS3 50 HLT 0.1 HLT
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
python FMS_dtaExplore.py $USR $DRV $QNT $AOI $THS $TRC
python FMS_dtaTraces.py $USR $DRV $QNT $AOI