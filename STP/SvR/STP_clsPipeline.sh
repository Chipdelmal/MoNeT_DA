#!/bin/bash

# MTR="WOP"
# THS="0.5"
# VT_SPLIT="0.3"
# KFOLD="50"

MTR=$1
THS=$2
VT_SPLIT="0.3"
KFOLD="50"

declare -a quantiles=("50")
for QNT in ${quantiles[@]}; do
   python STP_clsPreUnify.py $MTR $QNT
   python STP_clsPreprocess.py $MTR $QNT
   python STP_clsTrain.py $MTR $THS $VT_SPLIT $KFOLD $QNT
done
