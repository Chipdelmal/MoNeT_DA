# Pipelines Walthrough

When we analyze [MGDrivE](https://marshalllab.github.io/MGDrivE/)'s output, we...

##  Setup the experiment's structure

In general, we try to setup our experiments in nested folder structures (from [MGDrivE](https://marshalllab.github.io/MGDrivE/)):

```bash
EXPERIMENT_SET
    TRACES
        EXPERIMENT
            REPETITION
                001
                002
                ...
                N
    ANALYZED
        EXPERIMENT
    RAW 
```

The **TRACES** folder stores the information for each stochastic repetition of an experiment, whilst the **ANALYZED** one holds the mean response (or quantiles, if needed). The **RAW** folder is not used by any pipeline but stores the mating information of female mosquitoes.

To be able to parse the experiments easily in an automated way, we define the **EXPERIMENT** names following the convention:

```bash
E_V1_V2_V3_..._Vn
```

This convention was established to make factorial experiments easier to analyze, as each entry **V** represents the value of a particular variable (defined by our experimental requirements), and `E_` is a constant ID to make pattern-matching easy and streamlined. As a general rule, we keep the **V** variables as integers (multiplying the float values of the variables by a multiple of 10 if needed), and deal with the rescaling in our analysis pipelines.

## PreProcess

The initial step for every analysis pipeline is the **PreProcess** phase. This script takes the original CSV files and transforms them into more manageable and lightweight [compressed-pickle](https://pypi.org/project/compress-pickle/) files by aggregating the genetic and spatial information of the experiments.

```bash
EXPERIMENT_SET
    PREPROCESS
        E_V1_V2_V3_..._Vn-AOI_GRP_sum.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_srp.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_agg.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_spa.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_rep.bz
```

* sum (pkl): Aggregated mean data
* srp (pkl): Aggregated traces data
* agg (pkl): Landscape mean data (not aggregated spatially)
* rep (pkl): Landscape traces data (not aggregated spatially)
* spa (pkl): Landscape mean data reshapped by genotype (not aggregated spatially)



### Spatial Aggregation



### Genetic Aggregation





## PostProcess



* rto (npy): Ratio array repetitions data
* mlr (csv): Repetitions metrics (for ML workflow)
* qnt (csv): Quantiles metrics