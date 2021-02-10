
#!/bin/bash

# 1: USR
# 2: LND
# 3: Plots

python PYF_preProcess.py $1 PGS HLT $2
if [ "$3" = "True" ]; then
    python PYF_preTraces.py $1 PGS HLT $2
    python PYF_grids.py $1 PGS HLT $2 PRE
fi
