#!/bin/bash

# argv[1]: USR

python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'WOP' 'i_ren' 'i_res' 'i_sex'
python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'WOP' 'i_fch' 'i_fcb' 'i_ren'
python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'WOP' 'i_fcb' 'i_fcr' 'i_ren'

python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'CPT' 'i_ren' 'i_res' 'i_sex'
python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'CPT' 'i_fch' 'i_fcb' 'i_ren'
python STP_dtaHeatmap.py $1 'PAN' 'HLT' 'LDR' '50' 'CPT' 'i_fcb' 'i_fcr' 'i_ren'