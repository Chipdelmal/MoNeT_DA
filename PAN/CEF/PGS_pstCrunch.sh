#!/bin/bash

USR=$1
DRV=$2
AOI=$3
QNT=$4
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
python PGS_pstFraction.py $USR $DRV $AOI
python PGS_pstProcess.py $USR $DRV $AOI $QNT
python PGS_pstProcessML.py $USR $DRV $AOI $QNT