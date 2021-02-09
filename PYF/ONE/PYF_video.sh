#!/bin/bash

# argv1: User
# argv2: AOI
# argv3: Experiment

# ./STP_preVideo.sh dsk HLT E_016_024_200_000_000
python PYF_preVideo.py $1 PGS $2 SPA $3
python PYF_ffmpeg.py $1 PGS $2 SPA $3
