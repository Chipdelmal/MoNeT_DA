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
python CEF_pstFraction.py $USR $DRV $AOI
python CEF_pstProcess.py $USR $DRV $AOI $QNT
python CEF_pstProcessML.py $USR $DRV $AOI $QNT