#!/bin/bash

# argv1: User

python YDR_pstGrids.py $1 homing ASD
python YDR_pstGrids.py $1 homing XSD
python YDR_pstGrids.py $1 homing YSD
python YDR_pstGrids.py $1 shredder AXS
python YDR_pstGrids.py $1 shredder YXS