#!/bin/bash

QNT='50'
###############################################################################
# Data clean and compile
###############################################################################
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'TTI'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'TTO'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'WOP'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'CPT'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'POE'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'MNX'
python STP_clsUnify.py $1 'PAN' 'HLT' $QNT
###############################################################################
# Data pre-process
###############################################################################
python STP_clsPreprocess.py $1 'PAN' 'HLT' $QNT
###############################################################################
# Train Model
###############################################################################
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'CPT'
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'POE'
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'WOP'
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'TTI'
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'TTO'
python STP_clsTrain.py $1 'PAN' 'HLT' $QNT 'MNF'
