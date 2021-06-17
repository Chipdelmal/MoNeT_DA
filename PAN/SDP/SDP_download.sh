
DRV=$1
FNM='/home/chipdelmal/Documents/WorkSims/SDP'
SFN='/RAID5/marshallShare/SplitDrive_Suppression'

mkdir -p "${FNM}/${DRV}/000/img/preTraces"
mkdir -p "${FNM}/${DRV}/001/img/preTraces"

scp -r "lab:${SFN}/${DRV}/000/img/preTraces" "${FNM}/${DRV}/000/img/"
scp -r "lab:${SFN}/${DRV}/001/img/preTraces" "${FNM}/${DRV}/001/img/"

