#!/bin/bash
USR=$1
QNT=$2
THS=$3

###############################################################################
# Linked Drive
###############################################################################
bash tGD_clsProcess.sh $USR linkedDrive HLT $QNT
bash tGD_clsProcess.sh $USR linkedDrive WLD $QNT
bash tGD_clsProcess.sh $USR linkedDrive CST $QNT
bash tGD_clsProcess.sh $USR linkedDrive TRS $QNT
python tGD_clsUnify.py $USR linkedDrive HLT $QNT $THS
python tGD_clsUnify.py $USR linkedDrive WLD $QNT $THS
python tGD_clsUnify.py $USR linkedDrive CST $QNT $THS
python tGD_clsUnify.py $USR linkedDrive TRS $QNT $THS
###############################################################################
# Split Drive
###############################################################################
bash tGD_clsProcess.sh $USR splitDrive HLT $QNT
bash tGD_clsProcess.sh $USR splitDrive WLD $QNT
bash tGD_clsProcess.sh $USR splitDrive CST $QNT
bash tGD_clsProcess.sh $USR splitDrive TRS $QNT
python tGD_clsUnify.py $USR splitDrive HLT $QNT $THS
python tGD_clsUnify.py $USR splitDrive WLD $QNT $THS
python tGD_clsUnify.py $USR splitDrive CST $QNT $THS
python tGD_clsUnify.py $USR splitDrive TRS $QNT $THS
###############################################################################
# tGD
###############################################################################
# bash tGD_clsProcess.sh $USR tGD HLT $QNT
# bash tGD_clsProcess.sh $USR tGD WLD $QNT
# bash tGD_clsProcess.sh $USR tGD CST $QNT
# bash tGD_clsProcess.sh $USR tGD TRS $QNT
# python tGD_clsUnify.py $USR tGD HLT $QNT $THS
# python tGD_clsUnify.py $USR tGD WLD $QNT $THS
# python tGD_clsUnify.py $USR tGD CST $QNT $THS
# python tGD_clsUnify.py $USR tGD TRS $QNT $THS
 