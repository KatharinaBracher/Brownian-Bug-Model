#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N j_leadbetter
#
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -wd /home/s2603968/Brownian-Bug-Model
#
# Requested runtime allowance (of 1 hour)
#$ -l h_rt=01:00:00
#
# Request one GPU in the gpu queue:
#$ -q gpu 
#$ -pe gpu-a100 1
#
# Requested memory per core
#$ -l h_vmem=4G
#
# Email address for notifications
#$ -M s2603968@ed.ac.uk
#
# Option to request resource reservation
#$ -R y
#
# Where to pipe the python output to.
#$ -o pnn/model_gpu.out
#$ -e pnn/model_gpu.err

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda

# Load cuda
module load cuda/11.0.2

# Activate conda environment
source activate plankton

# Run the program
python PNN/model.py

