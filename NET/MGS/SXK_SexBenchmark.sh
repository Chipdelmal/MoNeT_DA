#!/bin/bash

USR=$1
LND="UNIF"
XID="SX"

###############################################################################
# Setting up path 
###############################################################################
if [ "$USR" == "dsk" ]; then
    PTH='/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/SX_BENCH/'
else
    PTH=''
fi

###############################################################################
# Generating landscapes loop
###############################################################################
for XNM in {1..5}; do
    XPPAT="${XID}${XNM}"
    echo "* Generating landscape: ${XPPAT}"
    python SXK_SexLandscape.py $PTH $LND $XPPAT
done