#!/bin/bash

QNT=$1

MTR="WOP"
THS="0.1"
VT_SPLIT="0.5"
KFOLD="20"

python STP_clsPreUnify.py $MTR $QNT
python STP_clsPreprocess.py $MTR $QNT
python STP_clsTrain.py $MTR $QNT $THS