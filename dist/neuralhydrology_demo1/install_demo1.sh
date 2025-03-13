#!/usr/bin/env bash

help()
{
  echo "
  Neural Hydrology example install script

  USAGE: install_demo.sh  DataDirectory  ExperimentsDirectory
  * "DataDirectory" is the directory where CAMELS-US dataset will be downloaded (14 GB)
  * "ExperimentsDirectory" is where neuralhydrology runs will be stored
"
}

if [[n $# -lt 2 ]]; then
  help
  exit 0
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATA_DIR=$(realpath $1)
EXP_DIR=$(realpath $2)
CAMELS_SCRIPT="wget-camels-20250127T1907.sh"

# Create directories
mkdir -p ${EXP_DIR}
mkdir -p ${DATA_DIR}

# Pull docker image
DEMO_IMAGE="ghcr.io/johnkit/neuralhydrology/demo1:1.0.0"
echo "Pulling container image ${DEMO_IMAGE} (6 GB) ..."
docker pull ${DEMO_IMAGE}

# Download CAMELS-US
echo "Downloading CAMEL-US dataset (14 GB) ..."
wget_script=${SOURCE_DIR}/.install/${CAMELS_SCRIPT}
cp ${wget_script} ${DATA_DIR}
cd ${DATA_DIR} && "./${CAMELS_SCRIPT}"

# Unzip contents
echo "Unzipping data ..."
cd ${DATA_DIR} && unzip basin_timeseries_v1p2_metForcing_obsFlow.zip

# Generate .args.txt file
ARGS_FILE=${SCRIPT_DIR}/app/demo1/.args.txt
echo "--data_dir" > ${ARGS_FILE}
echo ${DATA_DIR} >> ${ARGS_FILE}/basin_dataset_public_v1p2
echo "--experiments_dir" >> ${ARGS_FILE}
echo ${EXP_DIR} >> ${ARGS_FILE}

# Finis
echo "Install finished"
echo "To run:"
echo "  python3 app/demo1.py  -b BASIN_ID"
