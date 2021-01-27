#!/bin/bash

# argv1: User
# argv2: Release Composition
# argv3: Spatial Setting

# ./STP_pstTraces.sh srv 265 SPA v1
python STP_pstTraces.py $1 HLT $2 $3
python STP_pstTraces.py $1 TRS $2 $3
python STP_pstTraces.py $1 WLD $2 $3