#!/bin/bash

# argv1: User
# argv2: AOI
# argv3: Releases
# argv4: Land
# argv5: Experiment

# ./STP_preVideo.sh dsk HLT 106 SPA E_0025000000_03_0000000000_0100000000_0000015730
python STP_preVideo.py $1 $2 $3 $4 $5
python STP_ffmpeg.py $1 $2 $3 $4 $5