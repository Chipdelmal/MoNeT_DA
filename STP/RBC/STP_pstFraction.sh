#!/bin/bash

USR=$1
LND=$2
DRV=$3

python STP_pstFraction.py $USR HLT $LND $DRV
python STP_pstFraction.py $USR WLD $LND $DRV
python STP_pstFraction.py $USR TRS $LND $DRV