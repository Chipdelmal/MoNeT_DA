#!/bin/bash

# argv1: User
# argv2: THS


QNT="50"
bash ./YDR_pstTraces.sh $1 ASD $2 '0.1'
bash ./YDR_pstTraces.sh $1 YSD $2 '0.1'
bash ./YDR_pstTraces.sh $1 AXS $2 '0.1'
bash ./YDR_pstTraces.sh $1 YXS $2 '0.1'
bash ./YDR_pstTraces.sh $1 XSD $2 '0.1'
bash ./YDR_pstTraces.sh $1 CRS $2 '0.1'

bash ./YDR_pstGridsSet.sh $1
