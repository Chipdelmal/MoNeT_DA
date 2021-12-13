#!/bin/bash

USR=$1

tGD_preProcess.sh $USR tGD
tGD_preTraces.sh $USR tGD

tGD_preProcess.sh $USR linkedDrive
tGD_preTraces.sh $USR linkedDrive

tGD_preProcess.sh $USR splitDrive
tGD_preTraces.sh $USR splitDrive

