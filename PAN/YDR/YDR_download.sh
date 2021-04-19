#!/bin/bash

# argv1: Folder

# python YDR_download.py homing ASD $1
# python YDR_download.py homing XSD $1
# python YDR_download.py homing YSD $1
python YDR_download.py shredder AXS $1 $2
python YDR_download.py shredder CRS $1 $2
python YDR_download.py shredder YXS $1 $2
