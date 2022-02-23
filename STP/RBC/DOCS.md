# Documentation


## Simulations

The scripts required to generate the datasets for these experiments can be found at:

* [Panmictic LDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Grid_LDR.R)
* [Panmictic SDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Grid_SDR.R)
* [Spatial LDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Spatial_LDR.R)
* [Spatial SDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Spatial_SDR.R)

With the gene-cubes being:

* [LDR](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-CRISPR2MF.R)
* [SDR](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R)

These scripts export data to the following directories on the server:

* Panmictic raw data: `/RAID0/STP_Space_{LDR,SDR}/`
* Spatial raw data: `/RAID0/STP_Grid/{LDR,SDR}/PAN/000000/`

Which are symlinked at these locations for data analysis:

* Panmictic analysis: `/RAID5/marshallShare/STP_Grid/{LDR,SDR}/SPA/265_{S,D}{F,P,S}/`
* Spatial analysis: `/RAID5/marshallShare/STP_Grid/{LDR,SDR}/PAN/000000`


## Data Analysis

To run the PRE phases of the DA pipelines, use the following bash script:

```bash
./STP_crunchDataset.sh $USR LDR PAN True
./STP_crunchDataset.sh $USR SDR PAN True
```

