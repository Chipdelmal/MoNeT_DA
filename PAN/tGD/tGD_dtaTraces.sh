#!/bin/bash

USR=$1
QNT=$2
THS=$3
AOI=$4
PLT=$5

python tGD_dtaExploreMulti.py $USR 'linkedDrive' $AOI $QNT $THS
python tGD_dtaConverter.py $USR 'linkedDrive' $AOI $QNT $THS 'NM' $PLT
python tGD_dtaTraces.py $USR 'linkedDrive' $AOI $QNT $THS $PLT

python tGD_dtaExploreMulti.py $USR 'splitDrive' $AOI $QNT $THS
python tGD_dtaConverter.py $USR 'splitDrive' $AOI $QNT $THS 'NM' $PLT
python tGD_dtaTraces.py $USR 'splitDrive' $AOI $QNT $THS $PLT

python tGD_dtaExploreMulti.py $USR 'tGD' $AOI $QNT $THS
python tGD_dtaConverter.py $USR 'tGD' $AOI $QNT $THS 'NM' $PLT
python tGD_dtaTraces.py $USR 'tGD' $AOI $QNT $THS $PLT