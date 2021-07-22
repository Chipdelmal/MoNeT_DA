#!/bin/bash

USR=$1
DRV=$2
QNT=$3
CMP=$4
###############################################################################
# Data clean and compile
###############################################################################
if [[ "$CMP" = "True" ]]; then
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'TTI'
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'TTO'
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'WOP'
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'CPT'
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'POE'
    python STP_clsCompile.py $USR 'PAN' 'HLT' $DRV $QNT 'MNX'
    python STP_clsUnify.py $USR 'PAN' 'HLT' $DRV $QNT
fi
###############################################################################
# Data pre-process
###############################################################################
# python STP_clsPreprocess.py $USR 'PAN' 'HLT' $DRV $QNT
###############################################################################
# Train Model
###############################################################################
python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'CPT'
# python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'POE'
python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'WOP'
# python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'TTI'
# python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'TTO'
# python STP_clsTrain.py $USR 'PAN' 'HLT' $DRV $QNT 'MNF'
