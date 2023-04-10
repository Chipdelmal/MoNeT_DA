#!/bin/bash

USR=$1      # dsk
LND=$2      # Brikama
DRV="HUM"   # HUM/PGS
SPE='None'

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for aoi in "MRT0" "MRT1" "MRT2" "MRT3" "MRT4" "CSS0" "CSS1" "CSS2" "CSS3" "CSS4" 
do
    python GOP_preProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_intProcessEpi.py $USR $LND $DRV $aoi $SPE
    python GOP_preTraces.py $USR $LND $DRV $aoi $SPE
done
python GOP_intNumbersEpi.py $USR $LND $DRV "MRT0" $SPE '50'
python GOP_intNumbersEpi.py $USR $LND $DRV "CSS0" $SPE '50'