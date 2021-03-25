# SDP Split Drive Suppression (two nodes)

## Experiment Nomenclature

Folders and files follow this naming convention:

* `E_par_csa_csb_ren_res`
  * `par`: Parameters set
  * `csa`: Fitness cost A 
    * `SD/CRISPR`: Cas9
    * `Others`: male mating
  * `csb`: Fitness cost B
    * `SD/CRISPR`: gRNA
    * `Others`: lifespan
  * `ren`: Number of releases
  * `res`: Size of releases

For the breakdown of the **AOI** sets, look at the gene definitions:

* [(CRS) CRISPR](./SDP_gene_CRS.py)
* [(SDR) Split Drive](./SDP_gene_SDR.py)
* [(IIT) Wolbachia](./SDP_gene_IIT.py)
* [(PGS) pgSIT](./SDP_gene_PGS.py)
* [(FSR) fsRIDL](./SDP_gene_FSR.py)
* [(AXR) Autosomal X-Shredder](./SDP_gene_AXR.py)
* [(SIT) Sterile Insect Technique](./SDP_gene_SIT.py)