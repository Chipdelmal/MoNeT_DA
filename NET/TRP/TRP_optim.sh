#!/bin/bash

EXP='001'


for i in {1..9}
do
    python TRP_optim.py $EXP $i
done 

python TRP_optim.py $EXP 10
python TRP_optim.py $EXP 20
python TRP_optim.py $EXP 50

python TRP_devBrute.py $EXP