#!/bin/bash

cp -r /RAID5/marshallShare/pyf/ANALYZED/ /RAID5/marshallShare/pyf/PAN/
cp -r /RAID5/marshallShare/pyf/TRACE/ /RAID5/marshallShare/pyf/PAN/

cp -r /RAID5/marshallShare/pyf/ANALYZED/ /RAID5/marshallShare/pyf/SPA/
cp -r /RAID5/marshallShare/pyf/TRACE/ /RAID5/marshallShare/pyf/SPA/

rm -r /RAID5/marshallShare/pyf/ANALYZED
rm -r /RAID5/marshallShare/pyf/TRACE
