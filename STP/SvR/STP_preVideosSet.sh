#!/bin/bash

# argv1: User
# argv2: AOI
# argv3: Setting

bash ./STP_preVideo.sh $1 $2 $3 SPA E_0025000000_03_0000000000_0100000000_0000015730
bash ./STP_preVideo.sh $1 $2 $3 SPA E_0025000000_03_0000000000_0100000000_0000000000
bash ./STP_preVideo.sh $1 $2 $3 SPA E_0025000000_03_0000000000_0000000000_0000015730
bash ./STP_preVideo.sh $1 $2 $3 SPA E_0025000000_03_0000000000_0000000000_0000000000

./STP_preVideosSet.sh srv HLT 265