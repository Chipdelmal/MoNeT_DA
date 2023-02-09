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
for aoi in "MRT0" "MRT1" "MRT2" "MRT3" "MRT4" "MRT5" "CSS0" "CSS1" "CSS2" "CSS3" "CSS4" "CSS5"
do
    python GOP_preProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_intProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_preTraces.py $USR $LND $DRV $aoi $SPE
done
