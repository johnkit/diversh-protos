# Climate model notes

An informal attempt to understand the filename nomenclature for climate models

Example: `tas_Amon_CESM2_ssp585_r11i1p1f1_gn_201501-206412.nc`


## Google Gemini

tas_Amon_CESM2_ssp585_r11i1p1f1_gn_201501-206412.nc

The filename tas_Amon_CESM2_ssp585_r11i1p1f1_gn_201501-206412.nc is a common format for climate model output files, particularly those following the CMIP (Coupled Model Intercomparison Project) conventions. Let's break down the sections:

  * tas: This stands for "surface air temperature." It indicates the variable stored in the file. Other common variables include pr (precipitation), psl (sea level pressure), and tos (sea surface temperature).

  * _Amon_: This signifies the time frequency of the data. Amon means monthly averages. Other possibilities include day (daily), 3hr (3-hourly), 6hr (6-hourly), monclim (monthly climatology), etc.

  * CESM2_: This identifies the climate model that produced the data. CESM2 is the Community Earth System Model version 2, developed by the National Center for Atmospheric Research (NCAR).

  * ssp585_: This indicates the scenario used for the climate simulation. ssp585 refers to the Shared Socioeconomic Pathway 5-8.5. This scenario represents a high-emission future with relatively little mitigation of greenhouse gas emissions. Other SSPs exist (e.g., ssp126, ssp245, ssp370).

  * r11i1p1f1_: This is the realization, initialization, physics, and forcing index. It's a way to distinguish between different runs of the same model with slightly different initial conditions or parameter settings.

        r11: Realization 11. Different realizations represent different possible evolutions of the climate system given the same forcing scenario.
        i1: Initialization 1. Refers to the method of initializing the model.
        p1: Physics 1. Indicates a specific version of the model's physical parameterizations.
        f1: Forcing 1. Specifies the forcing dataset used.

  * gn_: This denotes the grid type. gn usually signifies a native grid, which is the model's original grid resolution. Other possibilities might include gr (grid, regridded to a standard resolution).

  * 201501-206412: This specifies the time period covered by the file. 201501 means January 2015, and 206412 means December 2064. The data in this file spans from January 2015 to December 2064.

  * .nc: This is the file extension, indicating that the file is in NetCDF (Network Common Data Format). NetCDF is a standard format for storing scientific data, particularly gridded data like climate model output. It's self-describing, meaning it contains metadata about the data it holds.

In summary, this filename tells us that the file contains monthly average surface air temperature data from the CESM2 model under the SSP585 scenario, from realization 11, initialized using method 1, with physics version 1, and forcing version 1, on the model's native grid, covering the period from January 2015 to December 2064. The data is stored in NetCDF format.


Also, for more about "ssp" numbers:
* https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways
* https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/Chapter2/section2.3_climate_model_uncertainty.html


## Google Search


From download_script.py
Vocabularies defined in https://github.com/WCRP-CMIP/CMIP6_CVs

### Variables

* tas:     near-surface air temperature (K)
* pr:      precipitaton (kg m-2 s-1)
* evspsbl: evaporation (kg m-2 s-1)

per https://na-cordex.org/variable-list.html

### Table ID

* Amon: monthly atmospheric variables

per https://help.ceda.ac.uk/article/4801-cmip6-data

### Source Activity

* CESM2: [Community Earth System Model 2](https://www.cesm.ucar.edu/models/cesm2)
* Grid 288 x 192 ? (lon/lat), 32 levels, per https://wcrp-cmip.github.io/CMIP6_CVs/docs/CMIP6_source_id.html

### SSPs

Shared Socioeconomic Pathways (SSPs)
https://climatedata.ca/resource/understanding-shared-socio-economic-pathways-ssps/

* 585: fossil-fueled development  (many challenges to mitigation, few challenges to adaptation)
* 245: middle-of-the-road development  (moderate challenges to both mitigation & adaptation)
* 126: sustainable development (few challenges to both mitigation & adaptation)

First digit is the SSP

Also
* https://en.wikipedia.org/wiki/Shared_Socioeconomic_Pathways
* https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/Chapter2/section2.3_climate_model_uncertainty.html


### RIP nomenclature (e.g. r11i1p1f1)

Index for variants (member of an ensemble of simulations)

r: realization (starting point)
i: initialization method
p: physics version
f:forcing

From https://confluence.ecmwf.int/display/CKB/CMIP%3A+Global+climate+projections#CMIP:Globalclimateprojections-Ensembles:

    Each modelling centre typically run the same experiment using the same model several times to confirm the robustness of results and inform sensitivity studies through the generation of statistical information. A model and its collection of runs is referred to as an ensemble. Within these ensembles, three different categories of sensitivity studies are done, and the resulting individual model runs are labelled by three integers indexing the experiments in each category.

        * The first category, labelled “realization”, performs experiments which differ only in random perturbations of the initialconditions of the experiment. Comparing different realizations allow estimation of the internal variability of the model climate.
        * The second category refers to variation in initialisation parameters. Comparing differently initialised output provides an estimate of how sensitive the model is to initial conditions.
        * The third category, labelled “physics”, refers to variations in the way in which sub-grid scale processes are represented. Comparing different simulations in this category provides an estimate of the structural uncertainty associated with choices in the model design.

    Each member of an ensemble is identified by a triad of integers associated with the letters r, i and p which index the “realization”, “initialization” and “physics” variations respectively. For instance, the member "r1i1p1" and the member "r1i1p2" for the same model and experiment indicate that the corresponding simulations differ since the physical parameters of the model for the second member were changed relative to the first member.

    It is very important to distinguish between variations in experiment specifications, which are globally coordinated across all the models contributing to CMIP5, and the variations which are adopted by each modelling team to assess the robustness of their own results. The “p” index refers to the latter, with the result that values have different meanings for different models, but in all cases these variations must be within the constraints imposed by the specifications of the experiment.

    For the scenario experiments, the ensemble member identifier is preserved from the historical experiment providing the initial conditions, so RCP 4.5 ensemble member “r1i1p2” is a continuation of historical ensemble member “r1i1p2”.

Other sources:
* https://earthscience.stackexchange.com/a/18421
* https://pmip4.lsce.ipsl.fr/doku.php/database:drs
* https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit?tab=t.0

### Grid

gn:  "data reported on a model's native grid"

per https://github.com/WCRP-CMIP/CMIP6_CVs/blob/main/CMIP6_grid_label.json

### Date Range

YYYYMM-YYYYMM


### Source code excerpt


```
base_urls = [
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r11i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r11i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r11i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r10i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r10i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r10i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://esgf-data1.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/NCAR/CESM2/ssp{scenario}/r4i1p1f1/Amon/{variable}/gn/v20200528/{variable}_Amon_CESM2_ssp{scenario}_r4i1p1f1_gn_201501-206412.nc",
        "filename": "{variable}_Amon_CESM2_ssp{scenario}_r4i1p1f1_gn_201501-206412.nc",
    },
    {
        "url": "https://aims3.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-CM6-1/ssp{scenario}/r4i1p1f2/Amon/{variable}/gr/v20190410/{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r4i1p1f2_gr_201501-210012.nc",
        "filename": "{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r4i1p1f2_gr_201501-210012.nc",
    },
    {
        "url": "https://aims3.llnl.gov/thredds/fileServer/css03_data/CMIP6/ScenarioMIP/CNRM-CERFACS/CNRM-CM6-1/ssp{scenario}/r6i1p1f2/Amon/{variable}/gr/v20190410/{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r6i1p1f2_gr_201501-210012.nc",
        "filename": "{variable}_Amon_CNRM-CM6-1_ssp{scenario}_r6i1p1f2_gr_201501-210012.nc",
    },
]

variables = ["tas", "pr", "evspsbl"]
scenarios = ["585", "245", "126"]
```
