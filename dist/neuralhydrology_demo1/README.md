# Neural Hydrology Demo1
March 2025

This package provides scripts to run the Google Neural Hydrology modeling tools
for watershed basins, using data recorded in the CAMELS-US dataset. The software
uses a container image at `ghcr.io/johnkit/neuralhydrology/demo1:1.0.0` to run
the pytorch computations. The image requries a container environment with GPU
support.

## Installing Demo1

To install, run the `install_demo1.sh` script, passing in 2 filesystem paths

```
USAGE: install_demo.sh  DataDirectory  ExperimentsDirectory
* "DataDirectory" is the directory where CAMELS-US dataset will be downloaded (14 GB)
* "ExperimentsDirectory" is where neuralhydrology runs will be stored
```

The `install_demo1.sh` script will:
  1. Pull the container image for running the pytorch training and testing (6.5 GB).
  2. Download and unzip the CAMELS-US dataset (14 GB).
  3. Create a file named `.args.txt` in the app directory, to store the locaions
     of the data and experiments directory.
  4. Copy a `run_install.sh` script to this directory.

## Running Demo1

A bash script is provided to run the demo. The only required input is the ID of one basin
in the CAMELS-US dataset.

```
run_demo1.sh  -b BASIN_ID
```

The `run_demo1.sh` script will:
  1. Train a LSTM model for the specified basin, using settings in the app/demo1/template.basin.yml file
  2. Test the LSTM model
  3. Output a netCDF file with the test results (observed and simulated streamflow).
     The location of the netcdf file will be listed at the end of the terminal output.

## Run Options

The bash script just calls a python script in the `app` directory. The usage for the python script is:


```
usage: demo1.py [-h] -d DATA_DIR -e EXPERIMENTS_DIR -b BASIN_ID [-r RUN_ID] [-t TRAINING_EPOCHS] [-n] [-v] [-l] [-k]

This script uses the demo1 container image to train and test neuralhyrology models. On turtleland4, use venv ~/.py3-venv/neuralhydrology

options:
  -h, --help            show this help message and exit
  -d DATA_DIR, --data_dir DATA_DIR
                        Path to CAMELS-US dataset
  -e EXPERIMENTS_DIR, --experiments_dir EXPERIMENTS_DIR
                        Directory for saving results
  -b BASIN_ID, --basin_id BASIN_ID
                        8-digit CAMELS-US basin id
  -r RUN_ID, --run_id RUN_ID
                        Run id for model (required for test step, not used for training)
  -t TRAINING_EPOCHS, --training_epochs TRAINING_EPOCHS
                        Number of training epochs [50]
  -n, --dry-run         Dry run (to check input args for validity)
  -v, --verbose         Print more info to stdout
  -l, --local_image_build
                        use locally built docker image
  -k, --keep_container  keep container running (dont stop)

Note: You can also put arguments in .args.txt file
```

## Plotting Results

The `plot_results.py` script is provided to generated simple plots of a trained model test results.
The script requires matplotlib and xarray packages.
The results for each run are written to a file named `test_results.nc` under the basin folder.
An example of the path is
`.../experiments/03164000/runs/run_0703_025058/test/model_epoch050/test_results.nc`
so the corresponding command is
`python3 plot_results.py .../experiments/03164000/runs/run_0703_025058/test/model_epoch050/test_results.nc`
