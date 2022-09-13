#!/bin/bash

USR=$1
DRV=$2
AOI=$3
QNT='50'

python PGS_pstFraction.py $USR $DRV $AOI
python PGS_pstProcess.py $URS $DRV $AOI $QNT