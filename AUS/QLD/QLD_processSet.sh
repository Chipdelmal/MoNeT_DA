#!/bin/bash

USR=$1
LND=$2
AOI="HLT"
###############################################################################
# New
###############################################################################
for scenario in "s1" "s2" "s3" "s4"; do
    python QLD_preProcess.py $USR $AOI $LND $scenario
    python QLD_preTraces.py $USR $AOI $LND $scenario
    # python QLD_pstFraction.py $USR $AOI $land $scenario
done
