#!/bin/bash

USR=$1

bash TPT_crunchData.sh $USR gambiae_0_low 0.1 
bash TPT_crunchData.sh $USR gambiae_10_low 0.1 
bash TPT_crunchData.sh $USR gambiae_20_low 0.1
bash TPT_crunchData.sh $USR gambiae_0_low 0.5 
bash TPT_crunchData.sh $USR gambiae_10_low 0.5 
bash TPT_crunchData.sh $USR gambiae_20_low 0.5

bash TPT_crunchData.sh $USR coluzzii_0_low 0.1 
bash TPT_crunchData.sh $USR coluzzii_10_low 0.1 
bash TPT_crunchData.sh $USR coluzzii_20_low 0.1
bash TPT_crunchData.sh $USR coluzzii_0_low 0.5 
bash TPT_crunchData.sh $USR coluzzii_10_low 0.5 
bash TPT_crunchData.sh $USR coluzzii_20_low 0.5

bash TPT_crunchData.sh $USR coluzzii_0_med 0.1
bash TPT_crunchData.sh $USR coluzzii_10_med 0.1
bash TPT_crunchData.sh $USR coluzzii_20_med 0.1
bash TPT_crunchData.sh $USR coluzzii_0_med 0.5
bash TPT_crunchData.sh $USR coluzzii_10_med 0.5
bash TPT_crunchData.sh $USR coluzzii_20_med 0.5
