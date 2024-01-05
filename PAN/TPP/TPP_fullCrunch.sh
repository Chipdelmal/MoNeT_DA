#!/bin/bash

USR=$1
MOS=$2
HUM=$3
THS=$4
###############################################################################
bash TPP_preCrunch.sh $USR $MOS $HUM
bash TPP_pstCrunch.sh $USR $MOS $HUM
bash TPP_clsCrunch.sh $USR $MOS $HUM $THS