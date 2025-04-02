#!/bin/bash

#SBATCH --job-name=yolo
#SBATCH --nodes=1
#SBATCH --partition=gpu_prod_long
#SBATCH --time=2:00:00
#SBATCH --output=logslurms/slurm-%A_%a.out
#SBATCH --error=logslurms/slurm-%A_%a.err
#SBATCH --exclude=sh00,sh[10-19]

python3 -m venv $TMPDIR/venv
source $TMPDIR/venv/bin/activate
python -m pip install ultralytics pylabel wandb

# Copy the data to local SSD
cp -r /mounts/Datasets3/Diatoms $TMPDIR/

sed -i "s:/mounts/Datasets3:$TMPDIR:" $TMPDIR/Diatoms/CleurieOrne/data.yaml

# modelname=yolo11x-obb.yaml
modelname=yolov8x-obb.yaml
batch=-1

yolo obb train data=$TMPDIR/Diatoms/CleurieOrne/data.yaml model=$modelname batch=$batch project=CleurieOrne
