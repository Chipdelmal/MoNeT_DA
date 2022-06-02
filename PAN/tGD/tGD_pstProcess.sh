#!/bin/bash

# argv1: User
# argv2: Drive
USR=$1
DRV=$2
QNT=$3

###############################################################################
# PstFraction
###############################################################################
python tGD_pstFraction.py $USR $DRV 'HLT' $QNT
python tGD_pstFraction.py $USR $DRV 'CST' $QNT
python tGD_pstFraction.py $USR $DRV 'TRS' $QNT
python tGD_pstFraction.py $USR $DRV 'WLD' $QNT
###############################################################################
# pstProcess
###############################################################################
python tGD_pstProcess.py $USR $DRV 'HLT' $QNT
python tGD_pstProcess.py $USR $DRV 'CST' $QNT
python tGD_pstProcess.py $USR $DRV 'TRS' $QNT
python tGD_pstProcess.py $USR $DRV 'WLD' $QNT
