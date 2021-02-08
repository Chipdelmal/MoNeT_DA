
#!/bin/bash

# 1: USR
# 2: LND

# PstFraction --------------------------------
python PYF_pstFraction.py $1 PGS HLT $2
# PstProcess ---------------------------------
# python PYF_pstProcess.py $1 PGS HLT $2 50
python PYF_pstProcess.py $1 PGS HLT $2 75
python PYF_pstProcess.py $1 PGS HLT $2 90
# PstPlots ------------------------------------
# python PYF_pstTraces.py $1 PGS HLT $2 50 0.1
python PYF_pstTraces.py $1 PGS HLT $2 75 0.1
python PYF_pstTraces.py $1 PGS HLT $2 90 0.1
python PYF_grids.py $1 PGS HLT $2 PST
# PstHeatmap ----------------------------------
# python PYF_pstHeatmap.py $1 PGS HLT $2 50 0.1
python PYF_pstHeatmap.py $1 PGS HLT $2 75 0.1
python PYF_pstHeatmap.py $1 PGS HLT $2 90 0.1
