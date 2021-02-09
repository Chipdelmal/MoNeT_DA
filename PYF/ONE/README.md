# Onetahi

Use of pgSIT technology on the [Onetahi](https://www.google.com/maps/place/Onetahi/@-17.0186371,-149.5998375,15z/data=!3m1!4b1!4m5!3m4!1s0x7690a7143905d5c1:0x428e6a6b59c3505c!8m2!3d-17.0188865!4d-149.5916056) island of PYF.

* [MGDrivE sim](https://github.com/Chipdelmal/MGDrivE/tree/master/Main/pyf)
* [Transforming insect population control with precision guided sterile males with demonstration in flies](https://www.researchgate.net/publication/330223336_Transforming_insect_population_control_with_precision_guided_sterile_males_with_demonstration_in_flies)
* [Reply to ‘Concerns about the feasibility of using “precision guided sterile males” to control insects’](https://www.researchgate.net/publication/335583021_Reply_to_'Concerns_about_the_feasibility_of_using_precision_guided_sterile_males_to_control_insects')

## Experiment Nomenclature

* `E_pop_ren_res_mad_mat`
  * `pop`: Population size (male and female) per node
  * `ren`: Number of weekly releases (x100)
  * `res`: Release size (fraction of the stable population x100)
  * `mad`: Adult lifespan reduction (x100)
  * `mat`: Male mating reduction (x100)

## Data Analysis Scripts

* `./PYF_preProcess.sh USR LND`
* `./PYF_pstProcess.sh USR LND`
* `./PYF_clsPipeline.sh USR LND`