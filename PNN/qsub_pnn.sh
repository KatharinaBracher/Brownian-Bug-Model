s#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N j_leadbetter
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -cwd
# Requested runtime allowance
#$ -l h_rt=00:20:00
# Requested memory (per core)
#$ -l h_vmem=4G
# Requested number of cores in parallel environment
#$ -pe sharedmem 2
# Email address for notifications
#$ -M s2603968@ed.ac.uk
# Option to request resource reservation
#$ -R y

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda
# Activate conda environment
conda activate plankton

# Run the program
python Brownian-Bug-Model/PNN/model_training.py