#!/bin/bash

USR=$1
DRV=$2
LND=$3
DCE=$4
QNT='50'
THS='0.1'
###############################################################################
# Processing data
###############################################################################
# python STP_preProcess.py $USR 'HLT' $LND $DRV
# python STP_pstFraction.py $USR 'HLT' $LND $DRV
# python STP_pstProcess.py $USR 'HLT' $LND $DRV $QNT
# ###############################################################################
# # Generate dataframes
# ###############################################################################
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'TTI'
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'TTO'
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'WOP'
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'CPT'
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'POE'
# python STP_clsCompile.py $USR $LND 'HLT' $DRV $QNT 'MNX'
###############################################################################
# Unify dataframes
###############################################################################
if [[ "$LND" = "PAN" ]]; then
    python STP_clsUnify.py $USR $LND 'HLT' $DRV $QNT
    python STP_dtaAmend.py $USR $LND 'HLT' $DRV $QNT
    python STP_clsPreprocess.py $USR $LND 'HLT' $DRV $QNT
    if [[ "$DCE" = "True" ]]; then
        python STP_dtaDICE.py $USR $LND 'HLT' $DRV $QNT
    fi
fi
