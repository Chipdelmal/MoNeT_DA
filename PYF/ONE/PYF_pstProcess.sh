
#!/bin/bash

# 1: USR
# 2: PGS
# 3: LND
# 4: QNT

# PstFraction --------------------------------
python PYF_pstFraction.py $1 $2 HLT $3
# PstProcess ---------------------------------
python PYF_pstProcess.py $1 $2 HLT $3 50
python PYF_pstProcess.py $1 $2 HLT $3 75
python PYF_pstProcess.py $1 $2 HLT $3 90
# PstPlots ------------------------------------
# python PYF_pstTraces.py $1 $2 HLT $3 $4
# python PYF_grids.py $1 $2 HLT $3 PST