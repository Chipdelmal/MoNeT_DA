#!/bin/bash

# argv1: User
# argv2: Drive
USR=$1
DRV=$2
QNT=$3

###############################################################################
# pstProcess
###############################################################################
python3 tGD_pstProcessML.py $USR $DRV 'HLT' $QNT
python3 tGD_pstProcessML.py $USR $DRV 'CST' $QNT
python3 tGD_pstProcessML.py $USR $DRV 'TRS' $QNT
python3 tGD_pstProcessML.py $USR $DRV 'WLD' $QNT
