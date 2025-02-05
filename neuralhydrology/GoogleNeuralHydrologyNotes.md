# Google Neural Hydrology

## Links
* Blog: https://neuralhydrology.github.io/
* Repo: https://github.com/neuralhydrology/neuralhydrology
* Docs: https://neuralhydrology.readthedocs.io/en/latest/index.html

## Papers
* [Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks](https://hess.copernicus.org/articles/22/6005/2018/#bib1.bibx53)
* [CAMELS: Catchment Attributes and MEteorology for Large-sample Studies](https://gdex.ucar.edu/dataset/camels.html)
* [Daymet: Annual Climate Summaries on a 1-km Grid for North America, Version 4 R1](https://daac.ornl.gov/DAYMET/guides/Daymet_Annual_V4R1.html)


## Datasets
Instructions at https://neuralhydrology.readthedocs.io/en/latest/tutorials/data-prerequisites.html

### CAMELS US
* Catchment Attributes and MEteorology for Large-sample Studies
* turtleland4:/home/john/projects/divers-h/data/camels

#### basin_mean_forcing
Contains 3 subdirectories daymet, maurer, nldas
01013500_lump_cida_forcing_leap.txt
##### Daymet
[Daymet: Annual Climate Summaries on a 1-km Grid for North America, Version 4 R1](https://daac.ornl.gov/DAYMET/guides/Daymet_Annual_V4R1.html)

One file per HU, e.g., 01013500_lump_cida_forcing_leap.txt:

```
Year Mnth Day Hr dayl(s) prcp(mm/day) srad(W/m2) swe(mm) tmax(C) tmin(C) vp(Pa)
1980 01 01 12   30172.51        0.00    153.40  0.00    -6.54   -16.30  171.69
1980 01 02 12   30253.10        0.00    145.27  0.00    -6.18   -15.22  185.94
1980 01 03 12   30344.18        0.00    146.96  0.00    -9.89   -18.86  138.39
1980 01 04 12   30408.33        0.00    146.20  0.00    -10.98  -19.76  120.06
1980 01 05 12   30413.48        0.00    170.43  0.00    -11.29  -22.21  117.87
...
2014 12 26 12   29998.58        0.00    91.11   0.00    3.61    -0.50   590.58
2014 12 27 12   30042.52        0.00    103.01  0.00    2.15    -2.55   508.64
2014 12 28 12   30062.75        2.79    104.63  0.00    2.46    -3.70   461.44
2014 12 29 12   30067.20        0.02    193.62  0.00    -0.76   -16.03  175.39
2014 12 30 12   30067.89        0.00    180.57  0.00    -13.31  -23.54  90.01
2014 12 31 12   30107.30        0.00    185.32  0.00    -14.84  -25.60  80.00
```

##### Maurer

One file per HU, e.g., 01013500_lump_maurer_forcing_leap.txt

```
Year Mnth Day Hr        Dayl(s) PRCP(mm/day)    SRAD(W/m2)      SWE(mm) Tmax(C) Tmin(C) Vp(Pa)
1980 01 01 12   30172.48        0.00    205.62  0.00    -12.09  -12.09  148.41
1980 01 02 12   30253.07        0.00    203.98  0.00    -11.63  -11.63  145.29
1980 01 03 12   30344.16        0.00    214.92  0.00    -13.36  -13.36  119.77
1980 01 04 12   30408.34        0.00    181.85  0.00    -15.38  -15.38  105.83
1980 01 05 12   30413.49        0.00    225.56  0.00    -17.09  -17.09  81.93
...
2008 12 26 12   30042.51        0.30    213.27  0.00    -14.00  -14.00  79.55
2008 12 27 12   30062.74        6.17    209.35  0.00    -16.76  -16.76  90.17
2008 12 28 12   30067.20        3.39    203.57  0.00    -7.35   -7.35   240.96
2008 12 29 12   30067.89        0.47    218.40  0.00    -0.68   -0.68   373.59
2008 12 30 12   30107.29        0.74    210.71  0.00    -7.78   -7.78   185.05
2008 12 31 12   30139.89        0.22    222.02  0.00    -13.23  -13.23  110.02
```

##### nlds

One file per HU, e.g., 01013500_lump_maurer_forcing_leap.txt

```
Year Mnth Day Hr        Dayl(s) PRCP(mm/day)    SRAD(W/m2)      SWE(mm) Tmax(C) Tmin(C) Vp(Pa)
1980 01 01 12   30172.48        0.00    218.66  0.00    -13.04  -13.04  203.28
1980 01 02 12   30253.07        0.00    199.05  0.00    -10.93  -10.93  237.37
1980 01 03 12   30344.16        0.00    197.64  0.00    -13.60  -13.60  169.39
1980 01 04 12   30408.34        0.00    214.61  0.00    -16.53  -16.53  134.57
1980 01 05 12   30413.49        0.00    206.02  0.00    -17.60  -17.60  129.30
1980 01 06 12   30485.90        1.23    203.38  0.00    -20.35  -20.35  103.99
...
2014 12 26 12   29998.56        0.09    178.17  0.00    -0.38   -0.38   492.56
2014 12 27 12   30042.51        0.00    194.21  0.00    -2.07   -2.07   452.67
2014 12 28 12   30062.74        3.09    114.66  0.00    -1.04   -1.04   531.84
2014 12 29 12   30067.20        0.00    127.81  0.00    -5.42   -5.42   330.87
2014 12 30 12   30067.89        0.00    196.92  0.00    -16.23  -16.23  121.57
2014 12 31 12   30107.29        0.00    137.68  0.00    -20.24  -20.24  97.72
```

#### usgs_streamflow

One file per HU, e.g. 01013500_streamflow_qc.txt

```
01013500 1980 01 01   655.00 A
01013500 1980 01 02   640.00 A
01013500 1980 01 03   625.00 A
01013500 1980 01 04   620.00 A
01013500 1980 01 05   605.00 A
01013500 1980 01 06   585.00 A
...
01013500 2014 12 25  -999.00 M
01013500 2014 12 26  -999.00 M
01013500 2014 12 27  -999.00 M
01013500 2014 12 28  -999.00 M
01013500 2014 12 29  -999.00 M
01013500 2014 12 30  -999.00 M
01013500 2014 12 31  -999.00 M
```

### Hourly forcing and streamflow data
* turtleland4:/home/john/projects/divers-h/data/nldas/usgs-streamflow-nldas_hourly.nc
* 19 GB
* Hourly data from 1979-01-01 to 2019-03-14
* For 516 basins
* 352368 date entries
* 17 variables

```
['convective_fraction',
 'longwave_radiation',
 'potential_energy',
 'potential_evaporation',
 'pressure',
 'shortwave_radiation',
 'specific_humidity',
 'temperature',
 'total_precipitation',
 'wind_u',
 'wind_v',
 'qobs_mm_per_hour',
 'qobs_count',
 'qualifiers',
 'utcoffset_hours',
 'rel_deviation_from_camels',
 'qobs_CAMELS_mm_per_hour']
 ```

## Examples

### Introduction.ipynb

Trains a single HU 01022500 (specified in `1_basin.txt`)

Excerpts from `1_basin.yml`

```
# training, validation and test time periods (format = 'dd/mm/yyyy')
train_start_date: "01/10/1999"
train_end_date: "30/09/2008"
validation_start_date: "01/10/1980"
validation_end_date: "30/09/1989"
test_start_date: "01/10/1989"
test_end_date: "30/09/1999"

# Forcing product [daymet, maurer, maurer_extended, nldas, nldas_extended, nldas_hourly]
# can be either a list of forcings or a single forcing product
forcings:
  - maurer
  - daymet
  - nldas

dynamic_inputs:
  - PRCP(mm/day)_nldas
  - PRCP(mm/day)_maurer
  - prcp(mm/day)_daymet
  - srad(W/m2)_daymet
  - tmax(C)_daymet
  - tmin(C)_daymet
  - vp(Pa)_daymet

# which columns to use as target
target_variables:
  - QObs(mm/d)
```

## Notes

NSE is the [Nash-Sutcliffe model](https://en.wikipedia.org/wiki/Nash%E2%80%93Sutcliffe_model_efficiency_coefficient), an error metric for training models.
