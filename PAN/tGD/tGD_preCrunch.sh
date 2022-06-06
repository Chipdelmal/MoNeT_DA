#!/bin/bash
USR=$1

###############################################################################
# Linked Drive
###############################################################################
source tGD_preProcess.sh $USR linkedDrive
source tGD_preTraces.sh $USR linkedDrive
python tGD_overlays.py $USR linkedDrive
###############################################################################
# Split Drive
###############################################################################
source tGD_preProcess.sh $USR splitDrive
source tGD_preTraces.sh $USR splitDrive
python tGD_overlays.py $USR splitDrive
###############################################################################
# tGD
###############################################################################
source tGD_preProcess.sh $USR tGD
source tGD_preTraces.sh $USR tGD
python tGD_overlays.py $USR tGD


# /RAID5/marshallShare/tGD/20220602/linkedDrive/000/ANALYZED/