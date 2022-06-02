# tGD Drive-out

Expanding upon the ideas presented on: ["A transcomplementing gene drive provides a flexible platform for laboratory investigation and potential field deployment"](https://www.researchgate.net/publication/338653394_A_transcomplementing_gene_drive_provides_a_flexible_platform_for_laboratory_investigation_and_potential_field_deployment)


## Experiment Nomenclature

Folders and files follow this naming convention:

* `E_fcs_fcb_fga_fgb_cut_hdr_ren_res`
  * `fcs`: Fitness cost on the Cas9 allele (1e4)
  * `fcb`: Fitness cost on broken alleles at the Cas9 locus (1e4)
  * `fga`: Fitness cost on gRNA allele (1e4)
  * `fgb`: Fitness cost on broken alleles at the gRNA locus (1e4)
  * `cut`: Cutting rate (1e2)
  * `hdr`: Homing rate (1e2)
  * `ren`: Number of releases (1e0)
  * `res`: Size of releases (1e2)

For the breakdown of the **AOI** sets, look at the gene definitions:

<!-- * [ClvR](./tGD_gene_clvr.py) -->
* [Linked Drive](./tGD_gene_linked.py)
* [Split Drive](./tGD_gene_split.py)
* [tGD](./tGD_gene_tGD.py)

Exported metrics (**MOI**) for the drive are:

* **WOP**: Total sum of time below the threshold
* **TTI**: First break below the threshold
* **TTO**: Last break below the threshold
* **RAP**: Fraction of the population with the genes at given points of time
* **MNX**: Minimum and maximum of genes in the population

Summary statistic files follow this naming convention:

* `AOI_MOI_QNT_qnt.csv`

Where the main **AOI** was **HLT** (presence of mosquitoes) and the outputs (labels) are:

* **TTI, TTO, WOP**: Fraction's threshold for the metric to be true
* **RAP**: Fraction of present genotypes at given points (days) of the simulation
* **MNX**: Min/Max and days at which these are achieved

## Current Pipelines

The following lines should run the whole set of analysis for the current workflow:

```bash
./tGD_preCrunch.sh srv; \
./tGD_pstCrunch.sh srv 50 0.1; \
./tGD_clsCrunch.sh srv 50 0.1; \
./tGD_dtaTraces.sh srv 50 0.1 HLT HLT
```