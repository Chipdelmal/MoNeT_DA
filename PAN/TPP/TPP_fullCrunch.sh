#!/bin/bash

USR=$1
###############################################################################
bash TPP_preCrunch.sh $USR
bash TPP_pstCrunch.sh $USR
bash TPP_clsCrunch.sh $USR