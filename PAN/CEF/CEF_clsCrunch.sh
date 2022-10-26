#!/bin/bash

USR=$1
DRV=$2
AOI=$3
QNT=$4
THS=$5

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for mtr in "WOP" "CPT" "POE" "TTI" "TTO" "MNX"
do
    python CEF_clsCompile.py $USR $DRV $QNT $AOI $mtr
done
python CEF_clsUnify.py $USR $DRV $QNT $AOI $THS 
python CEF_dtaExplore.py $USR $DRV $QNT $AOI $THS $AOI
python CEF_dtaTraces.py $USR $DRV $QNT $AOI
###############################################################################
# Launch Scripts (ML)
###############################################################################
for mtr in "WOP" "CPT" "TTI" "TTO" "MNX"
do
    python CEF_clsCompileML.py $USR $DRV $AOI $mtr
done
python CEF_clsUnifyML.py $USR $DRV $AOI $THS 
###############################################################################
# Launch Scripts (SA)
###############################################################################
for mtr in "WOP" "CPT" "POE" "TTI"
do
    python CEF_saAnalyzer.py $USR $DRV $QNT $AOI $THS $mtr
done
###############################################################################
# Train ML
###############################################################################
for mtr in "WOP" "CPT" "TTI"
do
    python CEF_mlrTrainML.py $USR $DRV $AOI $THS $mtr
done
###############################################################################
# Plot SA
###############################################################################
for mtr in "WOP" "CPT" "TTI"
do
    python CEF_saPlotter.py $USR $DRV $QNT $AOI $THS $mtr
done