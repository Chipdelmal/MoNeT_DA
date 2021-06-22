
DRV=$1
FNM='/home/chipdelmal/Documents/WorkSims/SDP'
SFN='/RAID5/marshallShare/SplitDrive_Suppression'

mkdir -p "${FNM}/${DRV}/000/img/preGrids"
mkdir -p "${FNM}/${DRV}/001/img/preGrids"

scp -r "lab:${SFN}/${DRV}/000/img/preGrids" "${FNM}/${DRV}/000/img/"
scp -r "lab:${SFN}/${DRV}/001/img/preGrids" "${FNM}/${DRV}/001/img/"

