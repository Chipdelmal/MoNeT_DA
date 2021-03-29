#!/bin/bash

# argv1: User


bash ./YDR_pstProcess.py $1 ASD
bash ./YDR_pstProcess.py $1 XSD
bash ./YDR_pstProcess.py $1 YSD
bash ./YDR_pstProcess.py $1 AXS
bash ./YDR_pstProcess.py $1 YXS
