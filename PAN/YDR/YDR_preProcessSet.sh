#!/bin/bash

# argv1: USR


bash ./YDR_preProcess.sh $1 AXS
bash ./YDR_preProcess.sh $1 YXS
bash ./YDR_preProcess.sh $1 CRS
bash ./YDR_preProcess.sh $1 ASD
bash ./YDR_preProcess.sh $1 XSD
bash ./YDR_preProcess.sh $1 YSD

