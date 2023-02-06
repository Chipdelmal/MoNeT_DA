#!/bin/bash

USR=$1

bash TPT_crunchData.sh dsk coluzzii_0_low 0.1 
bash TPT_crunchData.sh dsk coluzzii_10_low 0.1 
bash TPT_crunchData.sh dsk coluzzii_20_low 0.1
bash TPT_crunchData.sh dsk coluzzii_0_low 0.5 
bash TPT_crunchData.sh dsk coluzzii_10_low 0.5 
bash TPT_crunchData.sh dsk coluzzii_20_low 0.5

bash TPT_crunchData.sh dsk coluzzii_0_med 0.1
bash TPT_crunchData.sh dsk coluzzii_10_med 0.1
bash TPT_crunchData.sh dsk coluzzii_20_med 0.1
bash TPT_crunchData.sh dsk coluzzii_0_med 0.5
bash TPT_crunchData.sh dsk coluzzii_10_med 0.5
bash TPT_crunchData.sh dsk coluzzii_20_med 0.5

bash TPT_crunchData.sh dsk gambiae_0_low 0.1 
bash TPT_crunchData.sh dsk gambiae_10_low 0.1 
bash TPT_crunchData.sh dsk gambiae_20_low 0.1
bash TPT_crunchData.sh dsk gambiae_0_low 0.5 
bash TPT_crunchData.sh dsk gambiae_10_low 0.5 
bash TPT_crunchData.sh dsk gambiae_20_low 0.5
