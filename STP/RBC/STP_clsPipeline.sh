#!/bin/bash

# STP_clsCompile.py
# STP_clsUnify.py
# STP_clsPreprocess.py
# STP_clsTrain.py

python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'TTI'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'TTO'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'WOP'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'CPT'
python STP_clsCompile.py $1 'PAN' 'HLT' '90' 'POE'