#!/bin/bash

USR=$1 # dsk
DRV=$2 # PGG
LND="Dummy" # Brikama
SPE='None'

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for aoi in "ECO" "HLT"
do
    python PGG_preProcess.py $USR $LND $DRV $aoi $SPE
    python PGG_preTraces.py $USR $LND $DRV $aoi $SPE
done