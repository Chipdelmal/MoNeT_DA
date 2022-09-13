#!/bin/bash

./QLD_processSet.sh srvA 01
./QLD_processSet.sh srvB 02

# ./QLD_panels.sh '/Users/sanchez.hmsc/Desktop/QLD/year3/'

# rsync -avr -e "ssh" --exclude '*.csv' "/Users/sanchez.hmsc/Desktop/QLD/year3" "lab:/RAID0/QLD_PANELS"
# rsync -avr -e "ssh" --exclude '*.csv' "/Users/sanchez.hmsc/Desktop/QLD/year4" "lab:/RAID0/QLD_PANELS"