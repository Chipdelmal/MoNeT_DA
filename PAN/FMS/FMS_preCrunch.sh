#!/bin/bash

USR=$1
DRV=$2

python FMS_preProcess.py $USR $DRV ECO
python FMS_preTraces.py $USR $DRV ECO