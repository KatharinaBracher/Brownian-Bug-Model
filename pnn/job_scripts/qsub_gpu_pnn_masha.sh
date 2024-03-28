#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N masha_bracher
#
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -wd /home/s2445937/Brownian-Bug-Model
#
# Requested runtime allowance.
#$ -l h_rt=24:00:00
#
# Request one GPU in the gpu queue:
#$ -q gpu 
#$ -pe gpu-a100 1
#
# Requested memory per core
#$ -l h_vmem=512G
#
# Email address for notifications
#$ -M s2445937@ed.ac.uk
#
# Option to request resource reservation
#$ -R y
#
# Where to pipe the python output to.
#$ -o pnn/models/masha/model_gpu.out
#$ -e pnn/models/masha/model_gpu.err

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda

# Load cuda
module load cuda/11.0.2

# Activate conda environment
source activate plankton

# Run the program
python -u pnn/model_masha.py

