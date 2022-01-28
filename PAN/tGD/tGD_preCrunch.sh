#!/bin/bash

USR=$1

source tGD_preProcess.sh $USR tGD
source tGD_preTraces.sh $USR tGD

source tGD_preProcess.sh $USR linkedDrive
source tGD_preTraces.sh $USR linkedDrive

source tGD_preProcess.sh $USR splitDrive
source tGD_preTraces.sh $USR splitDrive

