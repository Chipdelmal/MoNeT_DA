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
for mtr in "WOP" "CPT" "POE" "TTI" "TTO" "MNX"
do
    python FMS_clsCompile.py $USR $DRV $QNT $AOI $mtr
done
python FMS_clsUnify.py $USR $DRV $QNT $AOI $THS 