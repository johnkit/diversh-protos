# DIVERS-H Protos

Started Feb 2025

## neuralhydrology
Github workflow has neuralhydrology-image.yml to build docker image of
the Google NeuralHydrology package.

To build locally:

```
cd neuralhydrology
docker build -f neuralhydrology.dockerfile -t neuralhydrology:v1.11.0 --build-arg version=v1.11.0 .
```

## neuralhydrology/demo1

Basic demo for single basin train & test

```
cd neuralhydrology

python demo1/main.py -s train -b 02430085 -y

python demo1/main.py -s test -b 02430085 -y -r run_1502_194916
```

With .args.txt file:
```
--data_dir
/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2
--experiments_root_dir
/home/john/projects/divers-h/experiments
```



## Containerized neuralhydrology/demo1

To build
```
cd neuralhydrology/demo1
docker build -f local.demo1.dockerfile -t nh/demo1 .
```

To run
```
docker run --rm -it --gpus all \
  --mount type=bind,src=/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2,dst=/data \
  --mount type=bind,src=/home/john/projects/divers-h/docker_experiments,dst=/experiments \
  nh/demo1 \
  python local_demo1.py -s train -d /data -e /experiments -b 02430085 -y
```

To run inside the container:
```
docker run --rm -it --gpus all \
  --mount type=bind,src=/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2,dst=/data,readonly \
  nh/demo1 \
  bash
```

Omit `  --mount type=bind,src=/home/john/projects/divers-h/docker_experiments,dst=/experiments \`


Then:
* `python main.py -s train -d /data -e /experiments -b 02430085 -y`
* `python main.py -s test -d /data -e /experiments -b 02430085 -y -r <RUN_ID>`
