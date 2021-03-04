# Onetahi

Use of pgSIT technology on the [Onetahi](https://www.google.com/maps/place/Onetahi/@-17.0186371,-149.5998375,15z/data=!3m1!4b1!4m5!3m4!1s0x7690a7143905d5c1:0x428e6a6b59c3505c!8m2!3d-17.0188865!4d-149.5916056) island of the Tetiaroa atoll in French Polynesia.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Od2OibI8cfE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> 

Data sources and sims:

* [MGDrivE sim (scripts to generate datasets)](https://github.com/Chipdelmal/MGDrivE/tree/master/Main/pyf)
* [Transforming insect population control with precision guided sterile males with demonstration in flies](https://www.researchgate.net/publication/330223336_Transforming_insect_population_control_with_precision_guided_sterile_males_with_demonstration_in_flies)
* [Reply to ‘Concerns about the feasibility of using “precision guided sterile males” to control insects’](https://www.researchgate.net/publication/335583021_Reply_to_'Concerns_about_the_feasibility_of_using_precision_guided_sterile_males_to_control_insects')

## Experiment Nomenclature

Folders and files follow this naming convention:

* `E_pop_ren_res_mad_mat`
  * `pop`: Population size (male and female) per node
  * `ren`: Number of weekly releases (x100)
  * `res`: Release size (fraction of the stable population x100)
  * `mad`: Adult lifespan reduction (x100)
  * `mat`: Male mating reduction (x100)

For the breakdown of the **AOI** sets, look at the [pgSIT gene definition](https://github.com/Chipdelmal/MoNeT2/blob/main/PYF/ONE/PYF_gene_pgSIT.py).

Exported metrics (**MOI**) for the drive are:

* **POE**: Probability of elimination
* **WOP**: Total sum of time below the threshold
* **TTI**: First break below the threshold
* **TTO**: Last break below the threshold
* **RAP**: Fraction of the population with the genes at given points of time
* **MNX**: Minimum and maximum of genes in the population

Summary statistic files follow this naming convention:

* `AOI_MOI_QNT_qnt.csv`

Where the main **AOI** was **HLT** (presence of mosquitoes).

## Data Analysis Scripts

* `./PYF_preProcess.sh USR LND PLOTS_BOOL`
* `./PYF_pstProcess.sh USR LND PLOTS_BOOL HEAT_BOOL`
* `./PYF_clsPipeline.sh USR LND`

## Machine Learning Dashboard

After running the [ML pipeline](./PYF_clsPipeline.sh), load the dashboard with:

`python PYF_clsApp.py PATH_TO_MODELS`

Go to `http://127.0.0.1:8050/`

## Outputs

![](https://raw.githubusercontent.com/Chipdelmal/MoNeT/master/docs/media/PYF_panel.png) <br><br>

![](https://raw.githubusercontent.com/Chipdelmal/MoNeT/master/docs/media/PYF_cages.png)