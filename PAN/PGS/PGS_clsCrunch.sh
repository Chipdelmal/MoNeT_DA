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
# for mtr in "WOP" "CPT" "POE" "TTI" "TTO" "MNX"
# do
#     python PGS_clsCompile.py $USR $DRV $QNT $AOI $mtr
# done
# python PGS_clsUnify.py $USR $DRV $QNT $AOI $THS 
# python PGS_dtaExplore.py $USR $DRV $QNT $AOI $THS $AOI
# python PGS_dtaTraces.py $USR $DRV $QNT $AOI
###############################################################################
# Launch Scripts (SA)
###############################################################################
# for mtr in "WOP" "CPT" "POE"
# do
#     python PGS_saAnalyzer.py $USR $DRV $QNT $AOI $THS $mtr
# done
###############################################################################
# Train ML
###############################################################################
# for mtr in "WOP" "CPT" "POE"
# do
#     python PGS_mlrTrainMLCleanQNT.py $USR $DRV $QNT $AOI $THS $mtr
# done
###############################################################################
# Launch Scripts (ML Complex)
###############################################################################
python PGS_pstProcessML.py $USR $DRV $AOI $QNT
for mtr in "WOP" "CPT" "TTI" "TTO" "MNX"
do
    python PGS_clsCompileML.py $USR $DRV $AOI $mtr
done
python PGS_clsUnifyML.py $USR $DRV $AOI $THS
# for mtr in "WOP" "CPT"
# do
#     python PGS_mlrTrainMLClean.py $USR $DRV $AOI $THS $mtr
# done
###############################################################################
# Plot
###############################################################################
# for mtr in "WOP" "CPT"
# do
#     python PGS_saPlotter.py $USR $DRV $QNT $AOI $THS $mtr
# done