#!/bin/bash

# EXP='004_STP'
EXP=$1
USR=$2

# python TRP_devBrute.py $EXP $USR

# python TRP_optim.py $EXP 50 $USR
# python TRP_optim.py $EXP 25 $USR
# python TRP_optim.py $EXP 20 $USR
# python TRP_optim.py $EXP 15 $USR
# python TRP_optim.py $EXP 10 $USR

# for i in {1..9}
# do
#     python TRP_optim.py $EXP $i $USR
# done 

python TRP_optimPlot.py $EXP 10 $USR