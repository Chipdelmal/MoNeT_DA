
#!/bin/bash

# 1: USR
# 2: PGS
# 3: LND
# 4: QNT

python PYF_pstProcess.py $1 $2 HLT $3 $4
python PYF_pstTraces.py $1 $2 HLT $3 $4
python PYF_grids.py $1 $2 HLT $3 PST