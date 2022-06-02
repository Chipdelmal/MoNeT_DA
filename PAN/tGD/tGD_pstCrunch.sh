#!/bin/bash
USR=$1
QNT='50'
THS='0.5'

source tGD_pstProcess.sh $USR 'linkedDrive' $QNT $THS
source tGD_pstProcess.sh $USR 'splitDrive' $QNT $THS
source tGD_pstProcess.sh $USR 'tGD' $QNT $THS
