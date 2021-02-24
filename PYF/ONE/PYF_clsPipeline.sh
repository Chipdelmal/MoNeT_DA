#!/bin/bash

# argv1: USR
# argv2: LND

MTR="WOP"
VT_SPLIT="0.25"
KFOLD="10"
QNT='90'

declare -a quantiles=("75" "90")
for QNT in ${quantiles[@]}; do
   python PYF_clsPreprocess.py $1 $2 $MTR $QNT
done

python PYF_clsTrain.py $1 $2 $MTR $QNT $VT_SPLIT $KFOLD