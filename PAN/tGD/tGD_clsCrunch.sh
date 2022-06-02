#!/bin/bash
USR=$1
QNT='50'

###############################################################################
# Linked Drive
###############################################################################
source tGD_clsProcess.sh $USR 'linkedDrive' 'HLT' $QNT
source tGD_clsProcess.sh $USR 'linkedDrive' 'WLD' $QNT
source tGD_clsProcess.sh $USR 'linkedDrive' 'CST' $QNT
source tGD_clsProcess.sh $USR 'linkedDrive' 'TRS' $QNT
###############################################################################
# Split Drive
###############################################################################
source tGD_clsProcess.sh $USR 'splitDrive' 'HLT' $QNT
source tGD_clsProcess.sh $USR 'splitDrive' 'WLD' $QNT
source tGD_clsProcess.sh $USR 'splitDrive' 'CST' $QNT
source tGD_clsProcess.sh $USR 'splitDrive' 'TRS' $QNT
###############################################################################
# tGD
###############################################################################
source tGD_clsProcess.sh $USR 'tGD' 'HLT' $QNT
source tGD_clsProcess.sh $USR 'tGD' 'WLD' $QNT
source tGD_clsProcess.sh $USR 'tGD' 'CST' $QNT
source tGD_clsProcess.sh $USR 'tGD' 'TRS' $QNT