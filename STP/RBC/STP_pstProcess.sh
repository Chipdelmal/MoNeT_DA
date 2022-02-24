#!/bin/bash

USR=$1
LND=$2
DRV=$3
QNT='50'

python STP_pstProcess.py $USR "HLT" $LND $DRV $QNT
python STP_pstProcess.py $USR "WLD" $LND $DRV $QNT
python STP_pstProcess.py $USR "TRS" $LND $DRV $QNT