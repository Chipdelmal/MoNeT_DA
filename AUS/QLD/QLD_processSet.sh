#!/bin/bash

AOI="HLT"
python QLD_preProcess.py $1 $AOI $2 s1
python QLD_preProcess.py $1 $AOI $2 s2
python QLD_preProcess.py $1 $AOI $2 s3
python QLD_preProcess.py $1 $AOI $2 s4

python QLD_preTraces.py $1 $AOI $2 s1
python QLD_preTraces.py $1 $AOI $2 s2
python QLD_preTraces.py $1 $AOI $2 s3
python QLD_preTraces.py $1 $AOI $2 s4

python QLD_pstFraction.py $1 $AOI $2 s1
python QLD_pstFraction.py $1 $AOI $2 s2
python QLD_pstFraction.py $1 $AOI $2 s3
python QLD_pstFraction.py $1 $AOI $2 s4
