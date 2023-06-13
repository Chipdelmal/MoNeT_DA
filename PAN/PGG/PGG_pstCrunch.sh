#!/bin/bash

USR=$1 # dsk
DRV=$2 # PGG
LND="Dummy" # Brikama
SPE='None'
AOI='HLT'
QNT=$3

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
python PGG_pstFraction.py $USR $LND $DRV $AOI $SPE
python PGG_pstProcess.py $USR $LND $DRV $AOI $SPE $QNT
