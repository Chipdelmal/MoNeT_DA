#!/bin/bash

# argv[1]: USR

USR=$1
DRV=$2

python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'WOP' 'i_ren' 'i_res' 'i_sex'
python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'WOP' 'i_fch' 'i_fcb' 'i_ren'
python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'WOP' 'i_fcb' 'i_fcr' 'i_ren'

python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'CPT' 'i_ren' 'i_res' 'i_sex'
python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'CPT' 'i_fch' 'i_fcb' 'i_ren'
python STP_dtaHeatmap.py $USR 'PAN' 'HLT' $DRV '50' 'CPT' 'i_fcb' 'i_fcr' 'i_ren'