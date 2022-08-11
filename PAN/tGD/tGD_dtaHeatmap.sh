#!/bin/bash

USR=$1
DRV=$2
QNT=$3
THS=$4

python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_ren' 'i_res' 'i_hdr'
python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_ren' 'i_res' 'i_hdr'

python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_hdr'
python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_ren'
python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_res'
python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_cut'
python tGD_dtaHeatmap.py $USR $DRV 'HLT' $QNT $THS 'CPT' 'i_fcs' 'i_hdr' 'i_cut'

python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_hdr'
python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_ren'
python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_res'
python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_fcs' 'i_fcb' 'i_cut'
python tGD_dtaHeatmap.py $USR $DRV 'TRS' $QNT $THS 'CPT' 'i_fcs' 'i_hdr' 'i_cut'