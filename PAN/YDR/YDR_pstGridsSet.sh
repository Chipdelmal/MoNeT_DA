#!/bin/bash

# argv1: User

QNT="75"
python YDR_pstGrids.py $1 homing ASD $QNT
python YDR_pstGrids.py $1 homing XSD $QNT
python YDR_pstGrids.py $1 homing YSD $QNT
python YDR_pstGrids.py $1 shredder AXS $QNT
python YDR_pstGrids.py $1 shredder YXS $QNT