# Pipelines Walthrough

WRITE AN INTRODUCTION

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

## Pre-Process

The initial step for every analysis pipeline is the **PreProcess** phase. This script takes the original CSV files and transforms them into more manageable and lightweight [compressed-pickle](https://pypi.org/project/compress-pickle/) files by aggregating the genetic and spatial information of the experiments (which will be explained in the following subsections). Running the pre-processing scripts generates a subset of the following files:

```bash
EXPERIMENT_SET
    PREPROCESS
        E_V1_V2_V3_..._Vn-AOI_GRP_sum.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_srp.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_agg.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_spa.bz
        E_V1_V2_V3_..._Vn-AOI_GRP_rep.bz
```

where **AOI** is the genotypical "analysis of interest" and the **GRP** is the spatial group (see the next section for an explanation). These files contain:

* **sum (pkl)**: Aggregated mean data
* **srp (pkl)**: Aggregated traces data
* **agg (pkl)**: Landscape mean data (not aggregated spatially)
* **rep (pkl)**: Landscape traces data (not aggregated spatially)
* **spa (pkl)**: Landscape mean data reshapped by genotype (not aggregated spatially)

Not all of them are needed for the post-processing routines to work, and some of them are partially deprecated as we have not been needing them in our latests works. The only two essential sets are: **sum** and **srp**.


### Spatial Aggregation

To understand the spread of genetic constructs we sometimes have to group a number of haunts together so that the data are easier to interpret (city blocks, villages, etcetera). Taking advantage of the fact that [MGDrivE](https://marshalllab.github.io/MGDrivE/) exports the nodes in a sequential order, we can do these aggregations quite easily by defining a list of lists that contains the position of the nodes to aggregate together. For example:

```python
LAND = ((0, 2, 4, 6), (1, 3, 5, 7))
```

would sum together the even nodes' information in **GRP** 0 and the odds in **GRP** 1. Please note that nodes are zero-indexed and that it corresponds to the lexicographical order in which the files are read and sorted into Python ([MGDrivE](https://marshalllab.github.io/MGDrivE/)'s output should conform to the same standard). These lists can be arbitrarily long and selected as needed by the specific geography or research question. In a simpler example, to do the analysis of a single-node population, we would define the landscape as:

```python
LAND = ((0), )
```

In our analyses, we store our geo-aggregation settings in a `EID_land.py` file (where **EID** is a three-letter code we define for the experiment) so that we can select amongst multiple geographies in the same analysis pipeline.

### Genetic Aggregation

Crucial to [MoNeT](https://github.com/Chipdelmal/MoNeT2) and [MGDrivE](https://marshalllab.github.io/MGDrivE/), the genetic aggregation is arguably the most complex element of the processing routines. In our pipelines, we define one "main" gene-selector file and as many sub-gene files as drive systems we consider in our analysis:

```bash
EID_gene.py
    EID_gene_DRV1.py
    EID_gene_DRV2.py
    ...
    EID_gene_DRVn.py
```

The main file contains the `driveSelector` function definition, that takes in the **DRV** (drive's ID), along with the the **AOI**; and returns the drive's aggregation dictionary, and the color palette to use for traces (needed and useful in heatmap routines, although not essential outside that scope).

```python
geneDict = {
    'gDict': aggregationDictionary, 
    'yRange': yRange, 
    'colors': colors, 
    'folder': folder
}
```

As mentioned before, the gene-aggregation files are the most complex in our pipelines, so we will spend a bit of time describing their rationale and options. To do so, we will use the ["linked-drive"](https://github.com/MarshallLab/MGDrivE/blob/master/MGDrivE/R/Cube-CRISPR2MF.R) (mutagenic chain reaction) drive **EID_gene_LDR**. This drive contains 10 different genotype combinations: 

```python
genotypes = ('WW', 'WH', 'WR', 'WB', 'HH', 'HR', 'HB', 'RR', 'RB', 'BB')
locus = (0, 1) 
```

Let's suppose we were interested in counting the frequencies of each different gene in the mosquito population at each time-step (an **AOI** that we usually call **ECO** for "ecology"). To do this, we would be interested in knowing how many mosquitoes are "WW", "WH", "WR", etcetera; and multiply the mosquitoes by the number of times each allele appears in their genotype ("WW" would be twice the "W" allele). To do this, we want to know where the genes appear in our locus (which is comprised by the 0 and 1 alleles in the genotype tags we defined in our [MGDrivE](https://marshalllab.github.io/MGDrivE/) [inheritance cube](https://github.com/MarshallLab/MGDrivE/blob/master/MGDrivE/R/Cube-CRISPR2MF.R)). Let's start by aggregating the "W" genes in the locus defined by the 0, 1 alleles:

```python
wGenes = (('W', locus), )
monet.aggregateGeneAppearances(genotypes, wGenes)
```

This would return the following list:

```python
[0, 0, 1, 2, 3]
```

which indicates that "W" appears (and will be counted) twice in the "WW" genotype (position 0 in the genotypes list), once in "WH", once in "WR and so forth. To do this for all the genes, we simply run:

```python
wGenes = (('W', locus), )
hGenes = (('H', locus), )
rGenes = (('R', locus), )
bGenes = (('B', locus), )
genesSlot = (wGenes, hGenes, rGenes, bGenes)
LDR_ECO = [monet.aggregateGeneAppearances(genotypes, i) for i in genesSlot]
```

If we were only interested in doing this **ECO** analyis, we could return the following structure:

```python
aggD = monet.generateAggregationDictionary(['W', 'H', 'R', 'B'], LDR_ECO)
```

in which the first list is the name our genes will take in the plot routines, and the second one our gene appearances list (they need to be sorted in the same way).

Now, let's say we are interested in determining if dominant disease-blocking gene "H" fixates in the mosquito population. In this case we're not interested in how many copies of the "H" allele a mosquito has, as compared to the other possible genes. We can do this easily by using the following code:

```python
hGenes = (('H', locus), )
oGenes = (('W', locus), ('R', locus), ('B', locus))
genesSlot = (hGenes, oGenes)
genesSets = [set(monet.aggregateGeneAppearances(genotypes, i)) for i in genesSlot]
LDR_HLT = [list(i) for i in (hPos, oPos - hPos, oPos | hPos)]
```

Breaking down this code, we start by counting "H" in one aggregation group and "all the other ones" in another one. Now, a slight modification with respect to the previous example is that we are casting the aggregation list as a set to remove duplicates. This has another important advantage, we can use set operations to remove the intersection of "H" from "Other" so that we have all the dominant appearances in the first collection, all the non-dominant in the second, and the whole count in the third. As a last step, we re-cast our genotypes collection as a list, so that it remains consistent with our whole pipeline.


## Post-Process

### Post-Fraction

* rto (npy): Ratio array repetitions data
* mlr (csv): Repetitions metrics (for ML workflow)
* qnt (csv): Quantiles metrics