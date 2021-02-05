
#!/bin/bash

# 1: USR
# 2: PGS
# 3: LND

python PYF_preProcess.py $1 $2 HLT $3
python PYF_preTraces.py $1 $2 HLT $3
python PYF_grids.py $1 $2 HLT $3 PRE