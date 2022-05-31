#!/bin/bash

USR=$1

# source tGD_preProcess.sh $USR linkedDrive
# source tGD_preTraces.sh $USR linkedDrive
# python tGD_overlays.py $USR linkedDrive

# source tGD_preProcess.sh $USR splitDrive
# source tGD_preTraces.sh $USR splitDrive
# python tGD_overlays.py $USR splitDrive

source tGD_preProcess.sh $USR tGD
source tGD_preTraces.sh $USR tGD
python tGD_overlays.py $USR tGD
