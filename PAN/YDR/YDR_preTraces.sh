#!/bin/bash

# argv1: User
# argv2: Gene Drive

expSet=$(./YDR_selector.sh $2)
# python3 YDR_preTraces.py $1 $expSet $2 ECO
python3 YDR_preTraces.py $1 $expSet $2 HLT
# python3 YDR_preTraces.py $1 $expSet $2 TRS
# python3 YDR_preTraces.py $1 $expSet $2 WLD

# python3 YDR_preGrids.py $1 $expSet $2