#!/bin/bash

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
# Launch Scripts
###############################################################################
bash CEF_preCrunch.sh $USR $DRV $AOI
bash CEF_pstCrunch.sh $USR $DRV $AOI $QNT
bash CEF_clsCrunch.sh $USR $DRV $AOI $QNT $THS