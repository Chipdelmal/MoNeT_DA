#!/bin/bash

USR=$1
QNT=$2
THS=$3
AOI=$4
PLT=$5

python tGD_dtaExplore.py $USR 'linkedDrive' $AOI $QNT $THS
python tGD_dtaConverter.py $USR 'linkedDrive' $AOI $QNT $THS 'NM' $PLT
python tGD_dtaTraces.py $USR 'linkedDrive' $AOI $QNT $THS $PLT