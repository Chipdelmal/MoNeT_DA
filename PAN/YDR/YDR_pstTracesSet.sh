#!/bin/bash

# argv1: User


bash ./YDR_pstTraces.py $1 ASD $2
bash ./YDR_pstTraces.py $1 XSD $2
bash ./YDR_pstTraces.py $1 YSD $2
bash ./YDR_pstTraces.py $1 AXS $2
bash ./YDR_pstTraces.py $1 YXS $2