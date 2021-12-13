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
for XNM in {1..2}; do
    XPPAT="${XID}${XNM}"
    echo "* Optimizing landscape: ${XPPAT}"
    python SXK_SexGA.py $PTH $LND $XPPAT "M"
    python SXK_SexGA.py $PTH $LND $XPPAT "F"
    python SXK_SexGA.py $PTH $LND $XPPAT "B"
done