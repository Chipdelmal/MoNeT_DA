#!/bin/bash

USR=$1
DRV=$2
###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
python FMS_preProcess.py $USR $DRV ECO
# python FMS_preTraces.py $USR $DRV ECO
python FMS_preProcess.py $USR $DRV HLT
python FMS_preTraces.py $USR $DRV HLT