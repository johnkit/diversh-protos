# nnhydrology notes

## Build docker image

`docker build -f nnhydrology.dockerfile -t nnhydrology/demo1 .`
`docker run -it --rm nnhydrology/demo1`

```
docker run -it --rm --gpus all \
  --mount type=bind,src=/home/john/projects/divers-h/data/camels/basin_dataset_public_v1p2,dst=/camels_us:ro \
  nnhydrology/demo1
```
Optionally add `nh-run --help`


## Runtime


`pod_nh  -c camels_dir  -r experiments_root_dir  -b basin_id  # train`
`pod_nh  -c camels_dir  -r experiments_root_dir  -x experiment_path  # test`


pod = PodNH(camels_dir, experiments_root_dir)
pod.train(basin_id)
