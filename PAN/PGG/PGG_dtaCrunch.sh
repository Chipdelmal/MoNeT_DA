#!/bin/bash

USR=$1 # dsk
DRV=$2 # PGS
LND='Dummy' # Brikama
SPE='None'
AOI='HLT'
QNT='50'
THS='0.1'

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Run Scripts
###############################################################################
for mtr in "WOP" "CPT" "POE" "TTI" "TTO" "MNX"
do
    python PGG_dtaCompile.py $USR $LND $DRV $AOI $SPE $QNT $mtr
done
python PGG_dtaUnify.py $USR $LND $DRV $AOI $SPE $QNT $THS
python PGG_dtaExplore.py $USR $LND $DRV $AOI $SPE $QNT $THS $AOI
python PGG_dtaTraces.py $USR $LND $DRV $AOI $SPE $QNT