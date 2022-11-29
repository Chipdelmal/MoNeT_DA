#!/bin/bash
USR=$1
DRV=$2

###############################################################################
# Linked Drive
###############################################################################
source tGD_preProcess.sh $USR $DRV
source tGD_preTraces.sh $USR $DRV
# # python tGD_overlays.py $USR linkedDrive
# ###############################################################################
# # Split Drive
# ###############################################################################
# source tGD_preProcess.sh $USR splitDrive
# source tGD_preTraces.sh $USR splitDrive
# # python tGD_overlays.py $USR splitDrive
# ###############################################################################
# # tGD
# ###############################################################################
# source tGD_preProcess.sh $USR tGD
# source tGD_preTraces.sh $USR tGD
# # python tGD_overlays.py $USR tGD
