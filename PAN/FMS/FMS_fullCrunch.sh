#!/bin/bash

USR=$1
DRV=$2
QNT=$3
THS=$4

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
bash FMS_preCrunch.sh $USR $drv
bash FMS_pstCrunch.sh $USR $drv $QNT
bash FMS_clsCrunch.sh $USR $drv $QNT HLT $THS
bash FMS_dtaTraces.sh $USR $drv $QNT HLT $THS HLT
bash FMS_dtaHeatmaps.sh $USR $drv $QNT HLT $THS 

