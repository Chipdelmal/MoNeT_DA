#!/bin/bash

python tGD_preProcess.py $1 $2 HLT
python tGD_preProcess.py $1 $2 CAP
python tGD_preProcess.py $1 $2 CST
python tGD_preProcess.py $1 $2 TRS
python tGD_preProcess.py $1 $2 WLD
python tGD_preProcess.py $1 $2 ECO
