#!/bin/bash

# ./QLD_processSet.sh dsk 02
# ./QLD_processSet.sh dsk3 01

./QLD_processSet.sh lab31 02
./QLD_processSet.sh lab33 01

./QLD_processSet.sh lab41 02
./QLD_processSet.sh lab43 01

./QLD_panels.sh '/Users/sanchez.hmsc/Desktop/QLD/year3/'
./QLD_panels.sh '/Users/sanchez.hmsc/Desktop/QLD/year4/'

rsync -avr -e "ssh" --exclude '*.csv' /Users/sanchez.hmsc/Desktop/QLD/year3 lab:/RAID0/QLD_PANELS
rsync -avr -e "ssh" --exclude '*.csv' /Users/sanchez.hmsc/Desktop/QLD/year4 lab:/RAID0/QLD_PANELS