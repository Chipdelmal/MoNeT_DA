#!/bin/bash

USR=$1
LND=$2
DRV=$3
QNT='50'
THS='0.1'

python STP_pstTraces.py $USR HLT $LND $DRV $QNT $THS
python STP_pstTraces.py $USR WLD $LND $DRV $QNT $THS
python STP_pstTraces.py $USR TRS $LND $DRV $QNT $THS

# python STP_pstGrids.py $1 $2 $QNT