#!/bin/bash

EXP=$1
USR=$2

# python TRP_brute.py $EXP $USR
python TRP_basePlot.py $EXP $USR

for i in {1..9}
do
    python TRP_optim.py $EXP $i $USR
done 

# python TRP_optim.py $EXP "10" $USR
# python TRP_optim.py $EXP "15" $USR
# python TRP_optim.py $EXP "20" $USR
# python TRP_optim.py $EXP "25" $USR
