#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N j_leadbetter_histograms
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -wd /home/s2603968/Brownian-Bug-Model
# Requested runtime allowance
#$ -l h_rt=24:00:00
# Requested memory (per core)
#$ -l h_vmem=64G
# Requested number of cores in parallel environment
#$ -pe sharedmem 4
# Email address for notifications
#$ -M s2603968@ed.ac.uk
#$ -m beas
# Option to request resource reservation
#$ -R y
# Where to pipe the python output to.
#$ -o histograms.out
#$ -e histograms.err

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda
# Activate conda environment
conda activate plankton

# Run the program
python -u histograms_eddie.py
