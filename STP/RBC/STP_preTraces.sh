#!/bin/bash

USR=$1
LND=$2
DRV=$3

python STP_preTraces.py $USR ECO $LND $DRV
python STP_preTraces.py $USR HLT $LND $DRV
python STP_preTraces.py $USR WLD $LND $DRV
python STP_preTraces.py $USR TRS $LND $DRV

# python STP_preGrids.py USR LND
