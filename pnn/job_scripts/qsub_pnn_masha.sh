#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N masha_bracher
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -wd /home/s2445937/Brownian-Bug-Model
# Requested runtime allowance
#$ -l h_rt=24:00:00
# Requested memory (per core)
#$ -l h_vmem=4G
# Requested number of cores in parallel environment
#$ -pe sharedmem 16
# Email address for notifications
#$ -M s2445937@ed.ac.uk
# Option to request resource reservation
#$ -R y
# Where to pipe the python output to.
#$ -o models/masha/model.out
#$ -e models/masha/model.err

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda
# Activate conda environment
conda activate plankton

# Run the program
python -u pnn/model_masha.py
