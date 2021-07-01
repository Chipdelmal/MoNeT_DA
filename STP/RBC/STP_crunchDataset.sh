#!/bin/bash

DRV=$1
QNT='50'
THS='0.1'
###############################################################################
# Processing data
###############################################################################
python STP_preProcess.py $1 'HLT' 'PAN' $DRV
python STP_pstFraction.py $1 'HLT' 'PAN' $DRV
python STP_pstProcess.py $1 'HLT' 'PAN' $DRV $QNT
###############################################################################
# Generate dataframes
###############################################################################
python STP_clsCompile.py $1 'PAN' 'HLT' $DRV $QNT 'TTI'
python STP_clsCompile.py $1 'PAN' 'HLT' $DRV $QNT 'TTO'
python STP_clsCompile.py $1 'PAN' 'HLT' $DRV $QNT 'WOP'
python STP_clsCompile.py $1 'PAN' 'HLT' $DRV $QNT 'CPT'
python STP_clsCompile.py $1 'PAN' 'HLT' $DRV $QNT 'POE'
###############################################################################
# Unify dataframes
###############################################################################
python STP_clsUnify.py $1 'PAN' 'HLT' $DRV $QNT
python STP_clsPreprocess.py $1 'PAN' 'HLT' $DRV $QNT
