
#!/bin/bash

QNT='50'
THS='0.1'

###############################################################################
# Processing data
###############################################################################
# python STP_preProcess.py $1 'HLT' 'PAN'
# python STP_pstFraction.py $1 'HLT' 'PAN'
# python STP_pstProcess.py $1 'HLT' 'PAN' $QNT
###############################################################################
# Generate dataframes
###############################################################################
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'TTI'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'TTO'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'WOP'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'CPT'
python STP_clsCompile.py $1 'PAN' 'HLT' $QNT 'POE'
###############################################################################
# Unify dataframes
###############################################################################
python STP_clsUnify.py $1 'PAN' 'HLT' $QNT
python STP_clsPreprocess.py $1 'PAN' 'HLT' $QNT
