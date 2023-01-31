#!/bin/bash

USR=$1 # dsk
LND=$2 # Brikama
DRV=$3 # HUM/PGS
SPE='None'

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for aoi in "CSS" "MRT"
do
    python GOP_preProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_intProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_preTraces.py $USR $LND $DRV $aoi $SPE
done
