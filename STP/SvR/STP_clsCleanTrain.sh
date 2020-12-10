#!/bin/bash


MTR="WOP"
THS="0.1"
VT_SPLIT="0.5"
KFOLD="20"


declare -a quantiles=("50" "70" "75" "85" "90" "95")
for QNT in ${quantiles[@]}; do
   python STP_clsPreUnify.py $MTR $QNT
   python STP_clsPreprocess.py $MTR $QNT
done

python STP_clsTrain.py $MTR $THS