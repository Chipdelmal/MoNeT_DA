#!/bin/bash

USR=$1
DRV=$2
AOI=$3

python PGS_preProcess.py $USR $DRV $AOI
python PGS_preTraces.py $USR $DRV $AOI