#!/bin/bash

USR=$1
DRV=$2
QNT=$3
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
python FMS_pstFraction.py $USR $DRV 'HLT'
python FMS_pstProcess.py $USR $DRV 'HLT' $QNT
python FMS_pstProcessML.py $USR $DRV 'HLT' $QNT