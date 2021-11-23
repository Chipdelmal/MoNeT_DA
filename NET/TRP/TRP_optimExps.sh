#!/bin/bash

# EXP='BASE-100'
# USR='dsk'

EXP=$1
USR=$2

# ./TRP_optim.sh "${EXP}-HOM" $USR
./TRP_optim.sh "${EXP}-HET" $USR

python TRP_concat.py $EXP $USR