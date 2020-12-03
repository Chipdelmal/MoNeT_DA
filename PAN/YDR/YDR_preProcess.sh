#!/bin/bash

# chmod +x YDR_preProcess.sh
expSet=$(./YDR_selector.sh $2)
python YDR_preProcess.py $1 $expSet $2 ECO
python YDR_preProcess.py $1 $expSet $2 HLT
python YDR_preProcess.py $1 $expSet $2 WLD
python YDR_preProcess.py $1 $expSet $2 TRS

if [ "$3" = "True" ]; then
	./YDR_preTraces.sh $1 $expSet $2
fi