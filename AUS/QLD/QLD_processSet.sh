#!/bin/bash

USR=$1
LND=$2
AOI="HLT"
###############################################################################
# Old
###############################################################################
# python QLD_preProcess.py $1 $AOI $2 s1
# ...
# python QLD_preProcess.py $1 $AOI $2 s4

# python QLD_preTraces.py $1 $AOI $2 s1
# ....
# python QLD_preTraces.py $1 $AOI $2 s4

# python QLD_pstFraction.py $1 $AOI $2 s1
# ...
# python QLD_pstFraction.py $1 $AOI $2 s4
###############################################################################
# New
###############################################################################
SCENARIOS=("s1" "s2" "s3" "s4")
for scenario in "${!SCENARIOS[@]}"; do
    python QLD_preProcess.py $USR $AOI $LND $scenario
    python QLD_preTraces.py $USR $AOI $LND $scenario
    python QLD_pstFraction.py $USR $AOI $LND $scenario
done