#!/bin/bash

# argv1: User
# argv2: Release Composition
# argv3: Spatial Setting
# argv4: MGDrivE Version

# ./STP_preProcess.sh srv 265 SPA v1
python STP_preTraces.py $1 HLT $2 $3 $4
python STP_preTraces.py $1 ECO $2 $3 $4
python STP_preTraces.py $1 TRS $2 $3 $4
python STP_preTraces.py $1 WLD $2 $3 $4

# argv1: User
# argv2: Release Composition
# argv3: Spatial Setting
# argv4: MGDrivE Version

python STP_preGrids.py $1 $2 $3
