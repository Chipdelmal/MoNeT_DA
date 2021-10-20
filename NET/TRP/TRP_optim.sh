#!/bin/bash

# EXP='004_STP'
EXP=$1

python TRP_optim.py $EXP 50
python TRP_optim.py $EXP 25
python TRP_optim.py $EXP 10

for i in {1..9}
do
    python TRP_optim.py $EXP $i
done 

python TRP_devBrute.py $EXP