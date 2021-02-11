
#!/bin/bash

# 1: USR
# 2: LND
# 3; Plots traces bool
# 4: Plots heatmaps bool

# PstFraction --------------------------------
python PYF_pstFraction.py $1 PGS HLT $2
# PstProcess ---------------------------------
# python PYF_pstProcess.py $1 PGS HLT $2 50
python PYF_pstProcess.py $1 PGS HLT $2 75
python PYF_pstProcess.py $1 PGS HLT $2 90
# PstPlots ------------------------------------
if [ "$3" = "True" ]; then
    # python PYF_pstTraces.py $1 PGS HLT $2 50 0.1
    # python PYF_pstTraces.py $1 PGS HLT $2 75 0.1
    python PYF_pstTraces.py $1 PGS HLT $2 90 0.1
    python PYF_grids.py $1 PGS HLT $2 PST
fi
# PstHeatmap ----------------------------------
if [ "$4" = "True" ]; then
    # python PYF_pstHeatmap.py $1 PGS HLT $2 50 0.1
    # python PYF_pstHeatmap.py $1 PGS HLT $2 75 0.1
    python PYF_pstHeatmap.py $1 PGS HLT $2 90 0.1 'A'
    python PYF_pstHeatmap.py $1 PGS HLT $2 90 0.1 'B'
fi