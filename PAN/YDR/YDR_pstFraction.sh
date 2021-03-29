#!/bin/bash

# argv1: User
# argv2: Gene Drive

expSet=$(./YDR_selector.sh $2)
python YDR_pstFraction.py $1 $expSet $2 HLT
python YDR_pstFraction.py $1 $expSet $2 TRS
python YDR_pstFraction.py $1 $expSet $2 WLD
