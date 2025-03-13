# Neural Hydrology Demo1
March 2025

## Installing Demo1

To install, run the `install_demo1.sh` script, passing in 2 filesystem paths

```
USAGE: install_demo.sh  DataDirectory  ExperimentsDirectory
* "DataDirectory" is the directory where CAMELS-US dataset will be downloaded (14 GB)
* "ExperimentsDirectory" is where neuralhydrology runs will be stored
```

This will pull the container image and download/unzip the CAMELS-US dataset.
The installer also creates a file named `.args.txt` in the app directory, which
stores the locations of the data and experiments directory

## Running Demo1

To run:

```
run_demo1.sh  -b BASIN_ID
```

The script will:
  1. Train a LSTM model for the specified basin, using settings in the app/demo1/template.basin.yml file
  2. Test the LSTM model
  3. Output a netCDF file with the test results (observed and simulated streamflow)

## Run Options

The bash script just calls a python script in the `app` directory The usage for the python script is:


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
````
