#!/bin/bash

USR=$1
XID=$2
LND=$3
TRP=$4

###############################################################################
# Setting up path 
###############################################################################
if [ "$USR" == "dsk" ]; then
    PTH='/home/chipdelmal/Documents/WorkSims/MGSurvE_Benchmarks/SX_BENCH/'
else
    PTH='/RAID5/marshallShare/MGS_Benchmarks/SX_BENCH'
fi

###############################################################################
# Generating landscapes loop
###############################################################################
for XNM in {1..1}; do
    XPPAT="${XID}${XNM}"
    echo "* Plotting landscape: ${XPPAT}"
    python SXK_SexPlot.py $PTH $LND $XPPAT $TRP "M"
    python SXK_SexPlot.py $PTH $LND $XPPAT $TRP "F"
    python SXK_SexPlot.py $PTH $LND $XPPAT $TRP "B"
done
