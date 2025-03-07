# DIVERS-H Protos

Started Feb 2025

## neuralhydrology
Github workflow has neuralhydrology-image.yml to build docker image of
the Google NeuralHydrology package.

To build locally:

`cd neuralhydrology`
`VERSION=$(cat neuralhydrology.version.txt) && docker build -f neuralhydrology.dockerfile -t neuralhydrology:${VERSION} .`


## neuralhydrology/demo1

Basic demo for single basin train & test

`cd neuralhydrology`
`python demo1/local_main.py -s train -b 02430085`
`python demo1/local_main.py -s test -b 02430085 -r run_1502_194916`

Will read .args.txt file if present. File contents, ,e.g.:
```
--data_dir
/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2
--experiments_root_dir
/home/john/projects/divers-h/experiments
```


## Containerized neuralhydrology/demo1

To build
`cd neuralhydrology/demo1`
`docker build -f demo1.dockerfile -t nh/demo1 .`


<!-- To run container
```
docker run --rm -it --gpus all \
  --mount type=bind,src=/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2,dst=/data \
  nh/demo1 \
  python local_demo1.py -s train -d /data -e /experiments -b 02430085
``` -->

To start container:
```
docker run --rm -it --gpus all \
  --mount type=bind,src=/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2,dst=/data,readonly \
  nh/demo1 \
  bash
```

Then:
* `python local_main.py -s train -d /data -e /experiments -b 02430085`
* `python local_main.py -s test -d /data -e /experiments -b 02430085 -r <RUN_ID>`
