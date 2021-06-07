#!/bin/bash

python QLD_preProcess.py dsk HLT 01 s1
python QLD_preProcess.py dsk HLT 01 s2
python QLD_preProcess.py dsk HLT 01 s3
python QLD_preProcess.py dsk HLT 01 s4

python QLD_preTraces.py dsk HLT 02 s1
python QLD_preTraces.py dsk HLT 02 s2
python QLD_preTraces.py dsk HLT 02 s3
python QLD_preTraces.py dsk HLT 02 s4


python QLD_preProcess.py dsk3 HLT 01 s1
python QLD_preProcess.py dsk3 HLT 01 s2
python QLD_preProcess.py dsk3 HLT 01 s3
python QLD_preProcess.py dsk3 HLT 01 s4

python QLD_preTraces.py dsk3 HLT 01 s1
python QLD_preTraces.py dsk3 HLT 01 s2
python QLD_preTraces.py dsk3 HLT 01 s3
python QLD_preTraces.py dsk3 HLT 01 s4