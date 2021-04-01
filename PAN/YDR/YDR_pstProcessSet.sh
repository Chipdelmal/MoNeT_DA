#!/bin/bash

# argv1: User


bash ./YDR_pstProcess.sh $1 ASD
bash ./YDR_pstProcess.sh $1 XSD
bash ./YDR_pstProcess.sh $1 YSD
bash ./YDR_pstProcess.sh $1 AXS
bash ./YDR_pstProcess.sh $1 YXS
