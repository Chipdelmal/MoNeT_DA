#!/bin/bash

###############################################################################
# Data clean and compile
###############################################################################
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'TTI'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'TTO'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'WOP'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'CPT'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'POE'
python STP_clsUnify.py $1 'PAN' 'HLT' '90'
###############################################################################
# Data pre-process
###############################################################################
python STP_clsPreprocess.py $1 'PAN' 'HLT' '90'
###############################################################################
# Train Model
###############################################################################
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'CPT'
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'POE'
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'POF'
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'WOP'
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'TTI'
python STP_clsTrain.py $1 'PAN' 'HLT' '90' 'TTO'