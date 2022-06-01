#!/bin/bash
USR=$1
QNT='50'
THS='10'

###############################################################################
# Linked Drive
###############################################################################
python tGD_pstFraction.py $USR 'linkedDrive' 'HLT' $QNT
python tGD_pstFraction.py $USR 'linkedDrive' 'CST' $QNT
python tGD_pstFraction.py $USR 'linkedDrive' 'TRS' $QNT
python tGD_pstFraction.py $USR 'linkedDrive' 'WLD' $QNT
###############################################################################
# Split Drive
###############################################################################
python tGD_pstFraction.py $USR 'splitDrive' 'HLT' $QNT
python tGD_pstFraction.py $USR 'splitDrive' 'CST' $QNT
python tGD_pstFraction.py $USR 'splitDrive' 'TRS' $QNT
python tGD_pstFraction.py $USR 'splitDrive' 'WLD' $QNT
###############################################################################
# tGD
###############################################################################
python tGD_pstFraction.py $USR 'tGD' 'HLT' $QNT
python tGD_pstFraction.py $USR 'tGD' 'CST' $QNT
python tGD_pstFraction.py $USR 'tGD' 'TRS' $QNT
python tGD_pstFraction.py $USR 'tGD' 'WLD' $QNT