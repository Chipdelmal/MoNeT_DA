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
bash PGS_preCrunch.sh $USR $DRV $AOI
bash PGS_pstCrunch.sh $USR $DRV $AOI $QNT
bash PGS_clsCrunch.sh $USR $DRV $AOI $QNT $THS