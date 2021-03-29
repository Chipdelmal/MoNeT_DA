#!/bin/bash

# argv1: User
# argv2: Gene Drive

expSet=$(./YDR_selector.sh $2)

python YDR_pstProcess.py $1 $expSet $2 HLT 50
python YDR_pstProcess.py $1 $expSet $2 TRS 50 
python YDR_pstProcess.py $1 $expSet $2 WLD 50

python YDR_pstProcess.py $1 $expSet $2 HLT 75
python YDR_pstProcess.py $1 $expSet $2 TRS 75 
python YDR_pstProcess.py $1 $expSet $2 WLD 75

python YDR_pstProcess.py $1 $expSet $2 HLT 90
python YDR_pstProcess.py $1 $expSet $2 TRS 90 
python YDR_pstProcess.py $1 $expSet $2 WLD 90