# TP-13 DA Files

To generate the whole analysis set for the paper, [run](./TPT_crunchData.sh):

```bash
TPT_crunchData.sh $USR
```

Upon the output of the simulation defined in [these MGDrive scripts](https://github.com/Chipdelmal/MGDrivE/tree/master/Main/TP13) (which make use of the [cubeHoming LDR](https://github.com/Chipdelmal/MGDrivE/blob/fb2106b7cfd52116121c8b6a4fa14ad360056e40/MGDri.vE/R/Cube-CRISPR2MF.R))

This will generate the required plots and summary files for:

* ECO: Gene frequencies
* HLT: Dominant transgene presence in female mosquitos
* HUM: Susceptible versus prevalence in humans
* INC: Human incidence analysis

Originally, the paths are set to be:

* `/RAID5/marshallShare/TP13` 
* `/RAID5/marshallShare/TP13`

But this can be changed in the [aux](./TPT_aux.py) file if needed.