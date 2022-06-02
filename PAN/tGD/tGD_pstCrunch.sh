#!/bin/bash
USR=$1
QNT=$2
THS=$3

source tGD_pstProcess.sh $USR 'linkedDrive' $QNT $THS
source tGD_pstProcess.sh $USR 'splitDrive' $QNT $THS
source tGD_pstProcess.sh $USR 'tGD' $QNT $THS
