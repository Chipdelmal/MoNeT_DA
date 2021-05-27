#!/bin/bash

# argv1: User
# argv2: Gene Drive

expSet=$(./YDR_selector.sh $2)
# python YDR_preProcess.py $1 $expSet $2 ECO
# python YDR_preProcess.py $1 $expSet $2 HLT
python YDR_preProcess.py $1 $expSet $2 TRS
# python YDR_preProcess.py $1 $expSet $2 WLD

if [ "$3" = "True" ]; then
    ./YDR_preTraces.sh "$@"
fi
