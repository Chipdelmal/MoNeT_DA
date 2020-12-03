#!/bin/bash

# chmod +x YDR_preTraces.sh
expSet=$(./YDR_selector.sh $2)
python YDR_preTraces.py $1 $expSet $2 ECO
python YDR_preTraces.py $1 $expSet $2 HLT
python YDR_preTraces.py $1 $expSet $2 WLD
python YDR_preTraces.py $1 $expSet $2 TRS
