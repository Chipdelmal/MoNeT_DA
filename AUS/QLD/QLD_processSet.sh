#!/bin/bash

USR=$1
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
for land in "01" "02"; do
    for scenario in "s1" "s2" "s3" "s4"; do
        python QLD_preProcess.py $USR $AOI $land $scenario
        python QLD_preTraces.py $USR $AOI $land $scenario
        # python QLD_pstFraction.py $USR $AOI $land $scenario
    done
done