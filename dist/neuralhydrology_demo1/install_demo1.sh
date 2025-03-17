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

if [[ $# -lt 2 ]]; then
  help
  exit 0
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATA_DIR=$(realpath $1)
EXP_DIR=$(realpath $2)

# Create directories
mkdir -p ${EXP_DIR}
mkdir -p ${DATA_DIR}

# Pull docker image
DEMO_IMAGE="ghcr.io/johnkit/neuralhydrology/demo1:1.0.0"
echo "Pulling container image ${DEMO_IMAGE} (6 GB) ..."
docker pull ${DEMO_IMAGE}

# Download CAMELS-US
echo "Downloading CAMEL-US dataset (3.2 GB) ..."
zip_filename="basin_timeseries_v1p2_metForcing_obsFlow.zip"
zip_url="https://gdex.ucar.edu/dataset/camels/file/${zip_filename}"
cd ${DATA_DIR} && wget ${zip_url}


# Unzip contents
echo "Unzipping data ..."
cd ${DATA_DIR} && unzip ${zip_filename}

# Generate .args.txt file
ARGS_FILE=${SCRIPT_DIR}/app/.args.txt
echo "--data_dir" > ${ARGS_FILE}
echo ${DATA_DIR}/basin_dataset_public_v1p2 >> ${ARGS_FILE}
echo "--experiments_dir" >> ${ARGS_FILE}
echo ${EXP_DIR} >> ${ARGS_FILE}

# Copy run_demo1.sh to this dir
cp ${SCRIPT_DIR}/.install/run_demo1.sh ${SCRIPT_DIR}

# Finis
echo "Install finished"
echo "To run:"
echo "  run_demo1.sh  -b BASIN_ID"
