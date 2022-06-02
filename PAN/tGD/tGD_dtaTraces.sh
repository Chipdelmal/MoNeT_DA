#!/bin/bash

USR=$1
AOI='HLT'
QNT='50'
THS='0.5'
TRC='HLT'

python tGD_dtaExplore.py $USR 'linkedDrive' $AOI $QNT $THS
python tGD_dtaConverter.py $USR 'linkedDrive' $AOI $QNT $THS 'NM' $TRC
python tGD_dtaTraces.py $USR 'linkedDrive' $AOI $QNT $THS $TRC