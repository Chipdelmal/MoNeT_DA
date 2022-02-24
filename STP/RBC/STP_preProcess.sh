#!/bin/bash

USR=$1
LND=$2
DRV=$3

python STP_preProcess.py $USR ECO $LND $DRV
python STP_preProcess.py $USR HLT $LND $DRV
python STP_preProcess.py $USR WLD $LND $DRV
python STP_preProcess.py $USR TRS $LND $DRV
