
#!/bin/bash

python PYF_preProcess.py $1 $2 HLT $3
python PYF_preTraces.py $1 $2 HLT $3
python PYF_grids.py $1 $2 HLT $3 PRE