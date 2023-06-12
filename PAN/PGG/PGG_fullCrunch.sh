#!/bin/bash

USR=$1
DRV='PGS'

bash PGG_preCrunch.sh $USR
bash PGG_pstCrunch.sh $USR $DRV