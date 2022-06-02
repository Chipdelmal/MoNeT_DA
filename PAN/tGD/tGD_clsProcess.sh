#!/bin/bash

USR=$1
DRV=$2
AOI=$3
QNT=$4
THS=$5

python tGD_clsCompile.py $USR $DRV $AOI $QNT 'WOP'
python tGD_clsCompile.py $USR $DRV $AOI $QNT 'CPT'
python tGD_clsCompile.py $USR $DRV $AOI $QNT 'TTI'
python tGD_clsCompile.py $USR $DRV $AOI $QNT 'TTO'
python tGD_clsCompile.py $USR $DRV $AOI $QNT 'MNX'
python tGD_clsCompile.py $USR $DRV $AOI $QNT 'POE'
